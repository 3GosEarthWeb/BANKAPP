from sqlalchemy.orm import Session
from app.models.audit_model import AuditLog


def log_action(
    db: Session,
    user_id: int = None,
    action: str = "",
    metadata: dict = None,
    ip_address: str = None,
    user_agent: str = None,
):
    """
    Logs a user or system action to the audit_logs table.

    Parameters:
    - user_id: The ID of the user performing the action (optional for system logs)
    - action: A short string describing the action (e.g. 'LOGIN_SUCCESS')
    - metadata: Optional dictionary with additional data
    - ip_address: Optional IP address of the request origin
    - user_agent: Optional user agent string
    """

    log = AuditLog(
        user_id=user_id,
        action=action,
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
