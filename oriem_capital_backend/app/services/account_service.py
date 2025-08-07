from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from decimal import Decimal
from typing import List

from app.models.account_model import Account
from app.schemas.account_schema import AccountCreate, AccountResponse, AccountUpdate

MINIMUM_DEPOSITS = {
    "checking": Decimal("25.00"),   # 🇺🇸 U.S. standard minimums
    "savings": Decimal("100.00")
}

def create_account(db: Session, user_id: int, data: AccountCreate) -> AccountResponse:
    # Enforce account type and minimum deposit
    account_type = data.account_type.lower()
    if account_type not in MINIMUM_DEPOSITS:
        raise ValueError("Invalid account type. Must be 'checking' or 'savings'.")

    min_required = MINIMUM_DEPOSITS[account_type]
    if data.initial_deposit < min_required:
        raise ValueError(f"Minimum deposit for {account_type} account is ${min_required:.2f}.")

    account = Account(
        user_id=user_id,
        account_type=account_type,
        balance=data.initial_deposit,
        nickname=data.nickname,
        status="active"
    )

    db.add(account)
    try:
        db.commit()
        db.refresh(account)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Account could not be created.")

    return account


def get_user_accounts(db: Session, user_id: int) -> List[AccountResponse]:
    return db.query(Account).filter(
        Account.user_id == user_id,
        Account.status != "closed"
    ).all()


def get_account_by_id(db: Session, user_id: int, account_id: int) -> AccountResponse:
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    return account


def update_account(db: Session, user_id: int, account_id: int, data: AccountUpdate) -> AccountResponse:
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    if data.nickname is not None:
        account.nickname = data.nickname

    if data.status is not None:
        if data.status not in ("active", "frozen", "closed"):
            raise HTTPException(status_code=400, detail="Invalid status.")
        account.status = data.status

    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, user_id: int, account_id: int):
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    # Soft delete — don't remove, just mark as closed
    account.status = "closed"
    db.commit()
