from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)
from sqlalchemy.orm import Session
from typing import Dict

from app.schemas.profile_schema import (
    ProfileUpdateRequest,
    PasswordChangeRequest,
    ProfileResponse,
    NotificationPreferenceRequest,
    LanguagePreferenceRequest
)
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_model import User
from app.database import get_db
from app.core.security import verify_password, hash_password

import shutil
import os
import uuid

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)

UPLOAD_DIR = "app/static/uploads/profiles"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """👤 Get the current user's profile"""
    return current_user


@router.put("/update", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """✏️ Update user's profile details"""
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/change-password", response_model=Dict[str, str])
def change_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🔒 Change user password securely"""
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    if payload.old_password == payload.new_password:
        raise HTTPException(status_code=400, detail="New password must be different")

    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@router.post("/upload-photo", response_model=Dict[str, str])
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """📸 Upload or update profile picture"""
    file_ext = os.path.splitext(file.filename)[-1]
    if file_ext.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Invalid file format")

    new_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Optionally store relative or public URL
    current_user.profile_photo_url = f"/static/uploads/profiles/{new_filename}"
    db.commit()

    return {"message": "Profile photo updated", "url": current_user.profile_photo_url}


@router.put("/set-language", response_model=Dict[str, str])
def set_language(
    payload: LanguagePreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🌍 Update user's language preference"""
    current_user.language = payload.language
    db.commit()
    return {"message": f"Language set to {payload.language}"}


@router.put("/notifications", response_model=Dict[str, str])
def update_notifications(
    payload: NotificationPreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🔔 Update user's email/SMS notification preferences"""
    current_user.notify_email = payload.notify_email
    current_user.notify_sms = payload.notify_sms
    db.commit()
    return {"message": "Notification preferences updated"}
