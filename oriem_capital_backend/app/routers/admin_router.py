from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.dependencies.auth_dependencies import get_current_admin
from app.models.user_model import User
from app.models.transaction_model import Transaction
from app.models.audit_model import AuditLog
from app.models.loan_model import Loan
from app.schemas.user_schema import UserResponse
from app.schemas.transaction_schema import TransactionResponse
from app.schemas.loan_schema import LoanResponse

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/dashboard", summary="Dashboard KPIs")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    users_count = db.query(User).count()
    tx_count = db.query(Transaction).count()
    total_tx_amount = db.query(func.sum(Transaction.amount)).scalar() or 0
    loans_count = db.query(Loan).count()
    loans_pending = db.query(Loan).filter(Loan.status == "pending").count()

    return {
        "users": users_count,
        "transactions": tx_count,
        "total_tx_volume": float(total_tx_amount),
        "loans_total": loans_count,
        "loans_pending": loans_pending,
    }


@router.get("/users", response_model=List[UserResponse])
def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/transactions", response_model=List[TransactionResponse])
def list_all_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/loans", response_model=List[LoanResponse])
def list_loans(
    status: str = Query(None, description="Filter by loan status (e.g., approved, pending, rejected)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    query = db.query(Loan).order_by(Loan.created_at.desc())
    if status:
        query = query.filter(Loan.status == status.lower())
    return query.offset(skip).limit(limit).all()


@router.get("/audit-logs", response_model=List[dict])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "metadata": log.metadata,
            "ip_address": log.ip_address,
            "created_at": log.created_at,
        } for log in logs
    ]
