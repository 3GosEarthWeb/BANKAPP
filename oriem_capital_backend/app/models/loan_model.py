from sqlalchemy import Column, Integer, Float, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    repaid = "repaid"
    defaulted = "defaulted"


class LoanType(str, enum.Enum):
    personal = "personal"
    business = "business"
    mortgage = "mortgage"
    auto = "auto"
    education = "education"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    type = Column(Enum(LoanType), default=LoanType.personal)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)

    status = Column(Enum(LoanStatus), default=LoanStatus.pending)
    purpose = Column(String, nullable=True)
    is_secured = Column(Boolean, default=False)
    contract_ref = Column(String, nullable=True, unique=True)

    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    disbursed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="loans", foreign_keys=[user_id])
    account = relationship("Account", foreign_keys=[account_id])
    repayments = relationship("LoanRepayment", back_populates="loan", cascade="all, delete-orphan")

    def to_audit_log(self):
        return {
            "action": "Loan Application",
            "user_id": self.user_id,
            "details": f"{self.type} loan for {self.amount} NGN - Status: {self.status}"
        }

    def to_admin_approval_log(self):
        return {
            "action": "Loan Approval",
            "admin_id": self.approved_by,
            "details": f"{self.status.upper()} {self.type} loan (ID: {self.id}) for user {self.user_id}"
        }
