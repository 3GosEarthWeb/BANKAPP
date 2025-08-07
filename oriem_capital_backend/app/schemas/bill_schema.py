# app/schemas/bill_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BillPaymentRequest(BaseModel):
    account_number: str
    bill_type: str  # e.g., electricity, airtime, TV
    provider: str   # e.g., MTN, DStv, PHCN
    amount: float
    reference: Optional[str] = None


class BillPaymentResponse(BaseModel):
    id: str
    user_id: int
    account_number: str
    bill_type: str
    provider: str
    amount: float
    reference: str
    status: str
    paid_at: datetime

    class Config:
        orm_mode = True
