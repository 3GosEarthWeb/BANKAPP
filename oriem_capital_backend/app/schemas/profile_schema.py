from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    language: Optional[str]


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


class LanguagePreferenceRequest(BaseModel):
    language: str


class NotificationPreferenceRequest(BaseModel):
    notify_email: bool
    notify_sms: bool


class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    language: Optional[str]
    profile_photo_url: Optional[str]
    notify_email: Optional[bool]
    notify_sms: Optional[bool]

    class Config:
        from_attributes = True  # ✅ for Pydantic v2
