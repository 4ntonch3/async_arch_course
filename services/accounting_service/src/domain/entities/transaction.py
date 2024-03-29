from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .billing_cycle import BillingCycle
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
    billing_cycle: BillingCycle
    type: TransactionType
    credit: Money
    debit: Money
    description: str
    created_at: datetime
