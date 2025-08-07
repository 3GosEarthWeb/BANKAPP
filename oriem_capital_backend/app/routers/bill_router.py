# app/routers/bill_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.bill_schema import BillPaymentRequest, BillPaymentResponse
from app.models.user_model import User
from app.models.bill_model import Bill
from app.models.account_model import Account
from app.dependencies.auth_dependencies import get_current_user
from app.database import get_db

from uuid import uuid4
from datetime import datetime

router = APIRouter(
    prefix="/api/bills",
    tags=["Bill Payments"]
)

@router.post("/pay", response_model=BillPaymentResponse, status_code=status.HTTP_201_CREATED)
def pay_bill(
    bill: BillPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's account
    account = db.query(Account).filter_by(user_id=current_user.id, account_number=bill.account_number).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    if account.balance < bill.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    # Deduct from balance
    account.balance -= bill.amount

    # Create bill record
    bill_record = Bill(
        id=str(uuid4()),
        user_id=current_user.id,
        account_number=account.account_number,
        bill_type=bill.bill_type,
        provider=bill.provider,
        amount=bill.amount,
        reference=bill.reference or str(uuid4()),
        status="paid",
        paid_at=datetime.utcnow()
    )
    db.add(bill_record)
    db.commit()
    db.refresh(bill_record)

    return bill_record
