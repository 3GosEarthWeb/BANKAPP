# app/services/bill_service.py

from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.bill_model import Bill
from app.schemas.bill_schema import BillCreateSchema, BillStatusUpdateSchema


def create_bill(user_id: int, payload: BillCreateSchema, db: Session):
    bill = Bill(
        id=str(uuid4()),
        user_id=user_id,
        bill_type=payload.bill_type,
        provider=payload.provider,
        amount=payload.amount,
        status="pending",
        scheduled_for=payload.scheduled_for,
        created_at=datetime.utcnow()
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def get_user_bills(user_id: int, db: Session):
    return db.query(Bill).filter_by(user_id=user_id).order_by(Bill.created_at.desc()).all()


def get_all_bills(db: Session):
    return db.query(Bill).order_by(Bill.created_at.desc()).all()


def update_bill_status(bill_id: str, payload: BillStatusUpdateSchema, db: Session):
    bill = db.query(Bill).filter_by(id=bill_id).first()
    if not bill:
        return None
    bill.status = payload.status
    db.commit()
    db.refresh(bill)
    return bill
