# app/utils/helpers.py

import random
import string
from datetime import datetime


def generate_account_number(length: int = 10) -> str:
    """Generate a random numeric account number."""
    return ''.join(random.choices(string.digits, k=length))


def get_current_timestamp() -> str:
    """Return the current timestamp as an ISO string."""
    return datetime.utcnow().isoformat()


def mask_email(email: str) -> str:
    """Mask an email for display: janedoe@example.com -> j***e@example.com"""
    try:
        name, domain = email.split("@")
        if len(name) <= 2:
            return "***@" + domain
        return name[0] + "***" + name[-1] + "@" + domain
    except Exception:
        return "***@***"


def mask_account_number(acc: str) -> str:
    """Mask account number for display: 1234567890 -> ******7890"""
    return '*' * (len(acc) - 4) + acc[-4:]


def format_currency(amount: float, currency: str = "₦") -> str:
    """Format amount as currency: ₦12,345.67"""
    return f"{currency}{amount:,.2f}"


def is_valid_phone(phone: str) -> bool:
    """Basic Nigerian phone number format validation."""
    return phone.startswith("+234") or phone.startswith("0") and phone[1:].isdigit()
