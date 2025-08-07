from app.models.failed_transaction_model import FailedTransaction
from app.models.audit_model import AuditLog
from sqlalchemy.orm import Session
from app.models.user_model import User
from datetime import datetime


def log_failed_transaction(db: Session, user: User, amount: float, reason: str):
    # Create failed transaction record
    failed_txn = FailedTransaction(
        user_id=user.id,
        amount=amount,
        reason=reason,
        timestamp=datetime.utcnow()
    )
    db.add(failed_txn)

    # Create audit log entry
    audit_entry = AuditLog(
        user_id=user.id,
        action="Failed Transaction",
        metadata=reason,
        timestamp=datetime.utcnow()
    )
    db.add(audit_entry)

    db.commit()
