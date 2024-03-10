from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .money import Money


class TransactionType(StrEnum):
    INCOME = "income"
    DEBIT = "debit"
    PAYOUT = "payout"


@dataclass
class Transaction:
    id: str
    public_id: str
    type: TransactionType
    created_at: datetime
    value: Money
