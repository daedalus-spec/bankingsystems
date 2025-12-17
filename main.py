from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend import models
from backend import schemas
from backend.database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Security configuration
SECRET_KEY = "secret-key-for-jwt-token-generation"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Atlas Holdings API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User endpoints
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/dashboard")
async def get_dashboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = db.query(models.Account).filter(models.Account.user_id == current_user.id).all()
    total_balance = sum(account.balance for account in accounts)
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).order_by(models.Transaction.created_at.desc()).limit(10).all()
    
    cards = db.query(models.Card).filter(models.Card.user_id == current_user.id).all()
    
    return {
        "user": current_user,
        "total_balance": total_balance,
        "accounts": accounts,
        "recent_transactions": transactions,
        "cards": cards
    }

# Account endpoints
@app.get("/accounts", response_model=List[schemas.Account])
async def get_accounts(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = db.query(models.Account).filter(models.Account.user_id == current_user.id).all()
    return accounts

@app.post("/accounts", response_model=schemas.Account)
async def create_account(account: schemas.AccountCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_account = models.Account(**account.dict(), user_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Transaction endpoints
@app.get("/transactions", response_model=List[schemas.Transaction])
async def get_transactions(
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).order_by(models.Transaction.created_at.desc()).offset(skip).limit(limit).all()
    return transactions

@app.post("/transactions", response_model=schemas.Transaction)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify account belongs to user
    account = db.query(models.Account).filter(
        models.Account.id == transaction.account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update account balance
    if transaction.transaction_type == "debit":
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= transaction.amount
    else:
        account.balance += transaction.amount
    
    db_transaction = models.Transaction(
        **transaction.dict(),
        user_id=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Card endpoints
@app.get("/cards", response_model=List[schemas.Card])
async def get_cards(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    cards = db.query(models.Card).filter(models.Card.user_id == current_user.id).all()
    return cards

@app.post("/cards", response_model=schemas.Card)
async def create_card(
    card: schemas.CardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_card = models.Card(**card.dict(), user_id=current_user.id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

# Bills endpoints
@app.get("/bills", response_model=List[schemas.Bill])
async def get_bills(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    bills = db.query(models.Bill).filter(models.Bill.user_id == current_user.id).all()
    return bills

@app.post("/bills", response_model=schemas.Bill)
async def create_bill(
    bill: schemas.BillCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_bill = models.Bill(**bill.dict(), user_id=current_user.id)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@app.put("/bills/{bill_id}/pay")
async def pay_bill(
    bill_id: int,
    account_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bill = db.query(models.Bill).filter(
        models.Bill.id == bill_id,
        models.Bill.user_id == current_user.id
    ).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if account.balance < bill.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Deduct from account
    account.balance -= bill.amount
    
    # Update bill status
    bill.is_paid = True
    bill.paid_at = datetime.utcnow()
    
    # Create transaction record
    transaction = models.Transaction(
        account_id=account_id,
        user_id=current_user.id,
        amount=bill.amount,
        transaction_type="debit",
        category=bill.category,
        description=f"Bill payment: {bill.name}"
    )
    db.add(transaction)
    
    db.commit()
    return {"message": "Bill paid successfully", "bill": bill}

# Analytics endpoints
@app.get("/analytics/income-outcome")
async def get_income_outcome(
    days: int = 7,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy import func
    start_date = datetime.utcnow() - timedelta(days=days)
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.created_at >= start_date
    ).all()
    
    daily_data = {}
    for transaction in transactions:
        date_key = transaction.created_at.strftime("%a")
        if date_key not in daily_data:
            daily_data[date_key] = {"income": 0, "outcome": 0}
        
        if transaction.transaction_type == "credit":
            daily_data[date_key]["income"] += float(transaction.amount)
        else:
            daily_data[date_key]["outcome"] += float(transaction.amount)
    
    return daily_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)