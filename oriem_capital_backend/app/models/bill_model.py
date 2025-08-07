# app/models/bill_model.py

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Bill(Base):
    __tablename__ = "bills"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String, index=True)
    bill_type = Column(String)      # e.g., electricity, airtime
    provider = Column(String)       # e.g., MTN, DStv
    amount = Column(Float)
    reference = Column(String, unique=True, index=True)
    status = Column(String, default="pending")
    paid_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bills")
