
# 📁 app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models.user_model import User, UserRole
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.core.jwt_handler import create_access_token, create_refresh_token
from app.core.email_service import send_verification_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================
# 🔐 Password Hashing
# =====================
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =====================
# 👤 User Registration
# =====================
def register_user(db: Session, data: RegisterRequest) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(data.password)

    new_user = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hashed_password,
        role=data.role or UserRole.customer,
        is_active=True,
        is_verified=False,  # Require verification before login
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email
    send_verification_email(new_user.email, new_user.id)
    return new_user


# =====================
# 🔑 User Authentication
# =====================
def authenticate_user(db: Session, data: LoginRequest) -> dict:
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name
        }
    }