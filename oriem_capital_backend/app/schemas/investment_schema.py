from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class InvestmentType(str, Enum):
    fixed_deposit = "fixed_deposit"
    mutual_fund = "mutual_fund"
    government_bond = "government_bond"
    corporate_bond = "corporate_bond"


class InvestmentStatus(str, Enum):
    active = "active"
    matured = "matured"
    withdrawn = "withdrawn"
    cancelled = "cancelled"


class InvestmentCreate(BaseModel):
    account_id: int
    type: InvestmentType
    amount: float
    interest_rate: float
    duration_months: int
    auto_renew: Optional[bool] = False
    notes: Optional[str]


class InvestmentWithdraw(BaseModel):
    investment_id: int
    notes: Optional[str]


class InvestmentResponse(BaseModel):
    id: int
    account_id: int
    type: InvestmentType
    amount: float
    interest_rate: float
    duration_months: int
    status: InvestmentStatus
    auto_renew: bool
    start_date: datetime
    maturity_date: Optional[datetime]
    withdrawn_date: Optional[datetime]
    notes: Optional[str]

    class Config:
        orm_mode = True
