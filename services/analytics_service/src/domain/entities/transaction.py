from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .money import Money
from .worker import Worker


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PAYMENT = "payment"


@dataclass
class Transaction:
    id: str
    public_id: str
    worker: Worker
    type: TransactionType
    created_at: datetime
    value: Money
