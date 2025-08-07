from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # nullable for system-level logs
    action = Column(String, nullable=False)  # e.g. 'LOGIN_SUCCESS', 'TRANSFER_FAILED'
    log_data = Column(JSON, nullable=True)   # ✅ renamed from 'metadata'

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="audit_logs")
