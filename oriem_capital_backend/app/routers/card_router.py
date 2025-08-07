# app/routers/card_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.database import get_db
from app.models.user_model import User
from app.models.card_model import Card
from app.models.account_model import Account
from app.schemas.card_schema import (
    CardRequestSchema,
    CardResponseSchema,
    CardStatusUpdateSchema
)
from app.dependencies.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/cards",
    tags=["Cards"]
)


@router.post("/request", response_model=CardResponseSchema, status_code=status.HTTP_201_CREATED)
def request_card(
    payload: CardRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate account
    account = db.query(Account).filter_by(account_number=payload.account_number, user_id=current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Check if card already exists
    existing_card = db.query(Card).filter_by(account_number=account.account_number, status="active").first()
    if existing_card:
        raise HTTPException(status_code=400, detail="Active card already exists for this account")

    # Create card
    new_card = Card(
        id=str(uuid4()),
        user_id=current_user.id,
        account_number=account.account_number,
        card_type=payload.card_type,
        issued_at=datetime.utcnow(),
        status="active"
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card


@router.get("/", response_model=list[CardResponseSchema])
def get_user_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cards = db.query(Card).filter_by(user_id=current_user.id).all()
    return cards


@router.put("/status", response_model=CardResponseSchema)
def update_card_status(
    payload: CardStatusUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter_by(id=payload.card_id, user_id=current_user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.status = payload.status
    db.commit()
    db.refresh(card)
    return card
