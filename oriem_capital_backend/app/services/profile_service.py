# app/services/profile_service.py

from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.profile_schema import ProfileUpdateSchema


def get_profile(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()


def update_profile(user_id: int, payload: ProfileUpdateSchema, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.full_name = payload.full_name or user.full_name
    user.phone = payload.phone or user.phone
    user.address = payload.address or user.address
    user.language = payload.language or user.language
    db.commit()
    db.refresh(user)
    return user
