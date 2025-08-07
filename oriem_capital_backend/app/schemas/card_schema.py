# app/schemas/card_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CardRequestSchema(BaseModel):
    account_number: str
    card_type: Literal["debit", "credit"] = "debit"


class CardStatusUpdateSchema(BaseModel):
    card_id: str
    status: Literal["active", "blocked"]


class CardResponseSchema(BaseModel):
    id: str
    user_id: int
    account_number: str
    card_type: str
    status: str
    issued_at: datetime

    class Config:
        orm_mode = True
