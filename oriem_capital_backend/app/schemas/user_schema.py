from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"


# ✅ Base user model for response
class UserBase(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True  # updated for Pydantic v2


# ✅ User profile update
class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True


# ✅ Admin-only user creation
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.customer  # default to customer
    phone: Optional[str] = None
    address: Optional[str] = None


# ✅ Login response schema
class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserBase


# ✅ Paginated user list for admin panel
class PaginatedUserList(BaseModel):
    total: int
    page: int
    per_page: int
    users: List[UserBase]


# ✅ Alias for backward compatibility
UserResponse = UserBase
