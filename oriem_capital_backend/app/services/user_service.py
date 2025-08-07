from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import user_model
from app.schemas.user_schema import UserUpdate
from app.services import audit_service


def get_user_by_id(db: Session, user_id: int) -> user_model.User:
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user_profile(db: Session, user_id: int, data: UserUpdate) -> user_model.User:
    user = get_user_by_id(db, user_id)

    if data.full_name is not None:
        user.full_name = data.full_name

    if data.email is not None:
        user.email = data.email

    if data.phone is not None:
        user.phone = data.phone

    if data.address is not None:
        user.address = data.address

    db.commit()
    db.refresh(user)

    audit_service.log_action(
        db=db,
        user_id=user_id,
        action="User Profile Updated",
        metadata=f"Updated fields: {data.dict(exclude_unset=True)}"
    )

    return user


def get_all_users(db: Session) -> list[user_model.User]:
    return db.query(user_model.User).all()


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()

    audit_service.log_action(
        db=db,
        user_id=user_id,
        action="User Deleted",
        metadata=f"User {user.email} deleted"
    )
