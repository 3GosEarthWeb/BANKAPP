# app/models/failed_transaction_model.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class FailedTransaction(Base):
    __tablename__ = "failed_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender_account_id = Column(Integer, nullable=True)
    receiver_account_id = Column(Integer, nullable=True)
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
