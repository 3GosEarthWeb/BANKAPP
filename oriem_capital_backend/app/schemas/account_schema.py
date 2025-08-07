from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from enum import Enum

class AccountType(str, Enum):
    checking = "checking"
    savings = "savings"

class AccountStatus(str, Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"

class AccountBase(BaseModel):
    account_type: AccountType
    nickname: Optional[str] = Field(None, example="Main Checking")

class AccountCreate(AccountBase):
    initial_deposit: Decimal = Field(..., gt=0, example=100.00)

class AccountUpdate(BaseModel):
    nickname: Optional[str] = Field(None, example="Vacation Savings")
    status: Optional[AccountStatus]

class AccountResponse(BaseModel):
    id: int
    account_type: AccountType
    nickname: Optional[str]
    balance: Decimal
    status: AccountStatus

    class Config:
        orm_mode = True
