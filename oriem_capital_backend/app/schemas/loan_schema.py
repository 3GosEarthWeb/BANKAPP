from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==============================
# 🧾 BASE SCHEMA
# ==============================

class LoanBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount requested")
    loan_type: str = Field(..., example="personal")
    term_months: int = Field(..., gt=0, description="Loan duration in months")
    purpose: Optional[str] = Field(None, example="Home renovation")


# ==============================
# 🧾 CREATE LOAN REQUEST
# ==============================

class LoanCreate(LoanBase):
    pass


# ==============================
# ✅ ADMIN APPROVAL INPUT
# ==============================

class LoanApproval(BaseModel):
    loan_id: int
    approve: bool
    admin_notes: Optional[str] = None


# ==============================
# 📤 RESPONSE SCHEMA
# ==============================

class LoanResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    loan_type: str
    term_months: int
    purpose: Optional[str]
    interest_rate: float
    status: str
    created_at: datetime
    approved_at: Optional[datetime]
    admin_notes: Optional[str] = None

    class Config:
        orm_mode = True
