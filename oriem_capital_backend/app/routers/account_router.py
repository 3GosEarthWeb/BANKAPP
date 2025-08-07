from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_model import User
from app.schemas.account_schema import AccountCreate, AccountResponse, AccountUpdate
from app.services import account_service

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["Accounts"]
)

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new checking or savings account for the authenticated user.
    """
    return account_service.create_account(db, user_id=current_user.id, data=data)


@router.get("/", response_model=List[AccountResponse])
def get_user_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all accounts owned by the current user.
    """
    return account_service.get_user_accounts(db, user_id=current_user.id)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific account by ID.
    """
    return account_service.get_account_by_id(db, user_id=current_user.id, account_id=account_id)


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    data: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update account nickname or status (if allowed).
    """
    return account_service.update_account(db, user_id=current_user.id, account_id=account_id, data=data)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Soft-delete an account (deactivates it, doesn't erase).
    """
    return account_service.delete_account(db, user_id=current_user.id, account_id=account_id)
