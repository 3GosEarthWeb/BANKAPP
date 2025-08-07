from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"
    international = "international"


class TransactionStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    reversed = "reversed"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="NGN")  # e.g. USD, EUR, NGN
    exchange_rate = Column(Float, nullable=True)  # only for international

    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.completed)

    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sender_account = relationship("Account", foreign_keys=[sender_account_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id])
    user = relationship("User", back_populates="transactions")

    def to_audit_log(self):
        return {
            "action": "Transaction",
            "user_id": self.user_id,
            "details": f"{self.type} of {self.amount} {self.currency} (Status: {self.status})"
        }
