# app/dependencies/auth_dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt_handler import decode_token
from app.database import get_db
from app.models import user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user = db.query(user_model.User).filter(user_model.User.id == payload.get("sub")).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    return user
