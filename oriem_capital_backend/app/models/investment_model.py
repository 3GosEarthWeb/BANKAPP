from sqlalchemy import Column, Integer, Float, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class InvestmentType(str, enum.Enum):
    fixed_deposit = "fixed_deposit"
    mutual_fund = "mutual_fund"
    government_bond = "government_bond"
    corporate_bond = "corporate_bond"


class InvestmentStatus(str, enum.Enum):
    active = "active"
    matured = "matured"
    withdrawn = "withdrawn"
    cancelled = "cancelled"


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    type = Column(Enum(InvestmentType), default=InvestmentType.fixed_deposit)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Annual interest rate in %
    duration_months = Column(Integer, nullable=False)

    status = Column(Enum(InvestmentStatus), default=InvestmentStatus.active)
    auto_renew = Column(Boolean, default=False)

    start_date = Column(DateTime(timezone=True), server_default=func.now())
    maturity_date = Column(DateTime(timezone=True), nullable=True)
    withdrawn_date = Column(DateTime(timezone=True), nullable=True)

    notes = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="investments")
    account = relationship("Account")

    def to_audit_log(self):
        return {
            "action": "Investment Created",
            "user_id": self.user_id,
            "details": f"{self.type} investment of ₦{self.amount} at {self.interest_rate}% for {self.duration_months} months"
        }
