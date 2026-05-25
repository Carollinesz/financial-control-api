from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ── Bank Account ──────────────────────────────────────────────────────────────

class BankAccountCreate(BaseModel):
    bank_name:   str
    bank_type:   str
    start_value: float = 0.0000


class BankAccountUpdate(BaseModel):
    bank_name:   str | None = None
    bank_type:   str | None = None
    start_value: float | None = None


class BankAccountRead(BankAccountCreate):
    model_config = ConfigDict(from_attributes=True)

    account_id: int


# ── Transaction ───────────────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    account_id:       int
    transaction_date: date
    value:            Decimal = Field(decimal_places=2)
    description:      str
    category:         str  | None = None
    type:             str  | None = None
    details:          dict | None = None


class TransactionUpdate(BaseModel):
    account_id:       int | None = None
    transaction_date: date | None = None
    value:            Decimal | None = Field(default=None, decimal_places=2)
    description:      str | None = None
    category:         str | None = None
    type:             str | None = None
    details:          dict | None = None


class TransactionRead(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
    created_at:     datetime
