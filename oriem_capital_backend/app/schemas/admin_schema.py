# app/schemas/admin_schema.py

from pydantic import BaseModel
from typing import Literal


class UserStatusUpdate(BaseModel):
    is_active: bool


class LoanApprovalRequest(BaseModel):
    status: Literal["approved", "rejected"]
