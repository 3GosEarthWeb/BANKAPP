# app/models/card_model.py

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String, nullable=False)
    card_type = Column(String, default="debit")  # debit or credit
    status = Column(String, default="active")    # active or blocked
    issued_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cards")
