from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import settings
from uuid import UUID

# === Settings ===
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_EXPIRE_DAYS = 7  # Or make this configurable


# === 🔐 Create Access Token ===
def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# === 🔄 Create Refresh Token ===
def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# === 🔓 Decode Token (Generic) ===
def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# === ✅ Verify Token and Role (RBAC helper) ===
def verify_token_and_role(token: str, required_roles: list[str] = None) -> Optional[dict]:
    payload = decode_token(token)
    if not payload:
        return None

    if required_roles:
        role = payload.get("role")
        if role not in required_roles:
            return None

    return payload
