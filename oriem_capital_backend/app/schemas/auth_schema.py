from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import UUID


# ============================
# 🔐 AUTH REQUEST SCHEMAS
# ============================

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: constr(min_length=8)  # type: ignore
    role: Optional[str] = "customer"

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "email": "jane@example.com",
                "password": "StrongPass123",
                "role": "customer"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jane@example.com",
                "password": "StrongPass123"
            }
        }


# ============================
# 🔐 AUTH RESPONSE SCHEMAS
# ============================

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    token: TokenResponse


# ============================
# 🔐 TOKEN PAYLOAD SCHEMA
# ============================

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


# ============================
# 👤 USER RESPONSE SCHEMA
# ============================

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    is_verified: bool

    class Config:
        from_attributes = True
