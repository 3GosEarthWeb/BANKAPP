from sqlalchemy import Column, String, Integer, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.customer)
    is_active = Column(Boolean, default=True)
    kyc_verified = Column(Boolean, default=False)

    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    accounts = relationship("Account", back_populates="owner", cascade="all, delete")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
bills = relationship("Bill", back_populates="user")
# user_model.py
cards = relationship("Card", back_populates="user")
