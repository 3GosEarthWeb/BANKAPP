# app/services/admin_service.py

from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.loan_model import Loan
from app.models.audit_model import AuditLog
from app.schemas.admin_schema import UserStatusUpdate, LoanApprovalRequest
from datetime import datetime


def get_all_users(db: Session):
    return db.query(User).all()


def update_user_status(user_id: int, payload: UserStatusUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user


def get_pending_loans(db: Session):
    return db.query(Loan).filter(Loan.status == "pending").all()


def approve_loan(loan_id: str, payload: LoanApprovalRequest, db: Session):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        return None
    loan.status = payload.status
    loan.approved_at = datetime.utcnow() if payload.status == "approved" else None
    db.commit()
    db.refresh(loan)
    return loan


def get_audit_logs(db: Session):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
