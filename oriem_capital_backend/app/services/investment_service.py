from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.investment_model import Investment, InvestmentStatus
from app.schemas.investment_schema import InvestmentCreate
from typing import List


def create_investment(db: Session, user_id: int, data: InvestmentCreate) -> Investment:
    maturity_date = datetime.utcnow() + timedelta(days=30 * data.duration_months)

    investment = Investment(
        user_id=user_id,
        account_id=data.account_id,
        type=data.type,
        amount=data.amount,
        interest_rate=data.interest_rate,
        duration_months=data.duration_months,
        auto_renew=data.auto_renew,
        maturity_date=maturity_date,
        notes=data.notes
    )
    db.add(investment)
    db.commit()
    db.refresh(investment)
    return investment


def withdraw_investment(db: Session, investment_id: int, user_id: int) -> Investment:
    investment = db.query(Investment).filter_by(id=investment_id, user_id=user_id).first()
    if not investment:
        raise Exception("Investment not found")

    if investment.status in [InvestmentStatus.withdrawn, InvestmentStatus.cancelled]:
        raise Exception("Investment already withdrawn or cancelled")

    investment.status = InvestmentStatus.withdrawn
    investment.withdrawn_date = datetime.utcnow()
    db.commit()
    db.refresh(investment)
    return investment


def list_user_investments(db: Session, user_id: int) -> List[Investment]:
    return db.query(Investment).filter_by(user_id=user_id).order_by(Investment.created_at.desc()).all()


def calculate_interest(investment: Investment) -> float:
    duration_years = investment.duration_months / 12
    return investment.amount * (investment.interest_rate / 100) * duration_years
