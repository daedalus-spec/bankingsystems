from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Account schemas
class AccountBase(BaseModel):
    account_number: str
    account_type: str
    currency: str = "USD"

class AccountCreate(AccountBase):
    balance: float = 0.0

class Account(AccountBase):
    id: int
    user_id: int
    balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transaction schemas
class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    category: Optional[str] = None
    description: Optional[str] = None
    recipient_name: Optional[str] = None

class TransactionCreate(TransactionBase):
    account_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int
    account_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Card schemas
class CardBase(BaseModel):
    card_number: str
    card_holder_name: str
    expiry_date: str
    cvv: str
    card_type: str = "debit"

class CardCreate(CardBase):
    balance: float = 0.0
    credit_limit: Optional[float] = None

class Card(CardBase):
    id: int
    user_id: int
    balance: float
    credit_limit: Optional[float]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bill schemas
class BillBase(BaseModel):
    name: str
    category: str
    amount: float
    due_date: Optional[datetime] = None
    recurring: bool = False

class BillCreate(BillBase):
    pass

class Bill(BillBase):
    id: int
    user_id: int
    is_paid: bool
    paid_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None