from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class LoanRepayment(Base):
    __tablename__ = "loan_repayments"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    paid_on = Column(DateTime, nullable=True)
    is_paid = Column(Boolean, default=False)

    loan = relationship("Loan", back_populates="repayments")
