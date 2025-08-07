from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from decimal import Decimal
import enum

class AccountTypeEnum(str, enum.Enum):
    checking = "checking"
    savings = "savings"

class AccountStatusEnum(str, enum.Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    balance = Column(Numeric(precision=12, scale=2), default=Decimal("0.00"))
    status = Column(Enum(AccountStatusEnum), default="active")

    nickname = Column(String(100), nullable=True)

    # Relationship
    user = relationship("User", back_populates="accounts")
