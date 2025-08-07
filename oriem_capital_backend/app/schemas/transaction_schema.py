from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"


class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


# ✅ Base response for any transaction
class TransactionResponse(BaseModel):
    id: int
    sender_account_id: Optional[int]
    receiver_account_id: Optional[int]
    user_id: int

    amount: float
    type: TransactionType
    status: TransactionStatus
    description: Optional[str]
    currency: str = "NGN"

    created_at: datetime

    class Config:
        orm_mode = True


# ✅ For creating a transfer
class TransferRequest(BaseModel):
    from_account_id: int = Field(..., description="Sender's account ID")
    to_account_id: int = Field(..., description="Receiver's account ID")
    amount: float = Field(..., gt=0)
    currency: Optional[str] = "NGN"
    description: Optional[str] = None


# ✅ For deposits
class DepositRequest(BaseModel):
    to_account_id: int
    amount: float = Field(..., gt=0)
    currency: Optional[str] = "NGN"
    description: Optional[str] = None


# ✅ For withdrawals
class WithdrawalRequest(BaseModel):
    from_account_id: int
    amount: float = Field(..., gt=0)
    currency: Optional[str] = "NGN"
    description: Optional[str] = None


# ✅ Paginated transaction history
class PaginatedTransactionList(BaseModel):
    total: int
    page: int
    per_page: int
    transactions: List[TransactionResponse]
