# app/services/card_service.py

from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.card_model import Card
from app.schemas.card_schema import CardRequestSchema, CardStatusUpdateSchema


def request_card(user_id: int, payload: CardRequestSchema, db: Session):
    card = Card(
        id=str(uuid4()),
        user_id=user_id,
        card_type=payload.card_type,
        status="pending",
        requested_at=datetime.utcnow()
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def get_user_cards(user_id: int, db: Session):
    return db.query(Card).filter(Card.user_id == user_id).order_by(Card.created_at.desc()).all()


def get_all_cards(db: Session):
    return db.query(Card).order_by(Card.created_at.desc()).all()


def update_card_status(card_id: str, payload: CardStatusUpdateSchema, db: Session):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return None
    card.status = payload.status
    db.commit()
    db.refresh(card)
    return card
