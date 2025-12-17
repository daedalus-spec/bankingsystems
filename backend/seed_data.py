from database import SessionLocal, engine
import models
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if data already exists
    existing_user = db.query(models.User).first()
    if existing_user:
        print("Database already seeded!")
        return
    
    # Create test user
    user = models.User(
        email="ahsan.jilani@dacatibank.com",
        full_name="Ahsan Jilani",
        hashed_password=pwd_context.hash("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {user.email}")
    
    # Create accounts
    accounts = [
        models.Account(
            user_id=user.id,
            account_number="1124456589917024",
            account_type="checking",
            balance=68657.00,
            currency="USD"
        ),
        models.Account(
            user_id=user.id,
            account_number="1124456589917025",
            account_type="savings",
            balance=25000.00,
            currency="USD"
        )
    ]
    
    for account in accounts:
        db.add(account)
    db.commit()
    print(f"Created {len(accounts)} accounts")
    
    # Create transactions
    transaction_data = [
        {"recipient": "Ahsan Jilani", "amount": -190, "category": "personal", "type": "debit"},
        {"recipient": "Furqan Ashiq", "amount": 270, "category": "transfer", "type": "credit"},
        {"recipient": "Ahtsahami", "amount": -150, "category": "shopping", "type": "debit"},
    ]
    
    for i, trans_data in enumerate(transaction_data):
        transaction = models.Transaction(
            user_id=user.id,
            account_id=accounts[0].id,
            amount=abs(trans_data["amount"]),
            transaction_type=trans_data["type"],
            category=trans_data["category"],
            recipient_name=trans_data["recipient"],
            description=f"Transaction with {trans_data['recipient']}",
            created_at=datetime.utcnow() - timedelta(days=i)
        )
        db.add(transaction)
    
    # Generate more transactions for chart data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        # Income transaction
        income = models.Transaction(
            user_id=user.id,
            account_id=accounts[0].id,
            amount=random.uniform(100, 500),
            transaction_type="credit",
            category="income",
            description=f"Income on {day}",
            created_at=datetime.utcnow() - timedelta(days=6-i)
        )
        db.add(income)
        
        # Outcome transaction
        outcome = models.Transaction(
            user_id=user.id,
            account_id=accounts[0].id,
            amount=random.uniform(50, 300),
            transaction_type="debit",
            category="expenses",
            description=f"Expenses on {day}",
            created_at=datetime.utcnow() - timedelta(days=6-i)
        )
        db.add(outcome)
    
    db.commit()
    print("Created transactions")
    
    # Create card
    card = models.Card(
        user_id=user.id,
        card_number="1124 8566 6989 1704",
        card_holder_name="Ahsan Jilani",
        expiry_date="12/26",
        cvv="123",
        card_type="debit",
        balance=68657.00
    )
    db.add(card)
    db.commit()
    print("Created card")
    
    # Create bills
    bills = [
        models.Bill(
            user_id=user.id,
            name="Water Bill",
            category="water",
            amount=45.50,
            due_date=datetime.utcnow() + timedelta(days=5),
            recurring=True
        ),
        models.Bill(
            user_id=user.id,
            name="Broadband Internet",
            category="broadband",
            amount=79.99,
            due_date=datetime.utcnow() + timedelta(days=10),
            recurring=True
        ),
        models.Bill(
            user_id=user.id,
            name="Electricity Bill",
            category="electricity",
            amount=125.00,
            due_date=datetime.utcnow() + timedelta(days=15),
            recurring=True
        )
    ]
    
    for bill in bills:
        db.add(bill)
    db.commit()
    print(f"Created {len(bills)} bills")
    
    db.close()
    print("\nDatabase seeded successfully!")
    print(f"Test user credentials:")
    print(f"Email: ahsan.jilani@dacatibank.com")
    print(f"Password: password123")

if __name__ == "__main__":
    seed_database()