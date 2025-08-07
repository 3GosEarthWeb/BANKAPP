from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services import investment_service
from app.schemas.investment_schema import InvestmentCreate, InvestmentResponse, InvestmentWithdraw
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_model import User

router = APIRouter(
    prefix="/api/v1/investments",
    tags=["Investments"]
)


@router.get("/", response_model=List[InvestmentResponse])
def get_user_investments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    📊 Get all investments for the logged-in user.
    """
    return investment_service.list_user_investments(db, user_id=current_user.id)


@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
def create_investment(
    data: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    💸 Create a new investment portfolio.
    """
    return investment_service.create_investment(db, user_id=current_user.id, data=data)


@router.put("/withdraw", response_model=InvestmentResponse)
def withdraw_investment(
    data: InvestmentWithdraw,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🚫 Withdraw or cancel an active investment.
    """
    return investment_service.withdraw_investment(db, investment_id=data.investment_id, user_id=current_user.id)
