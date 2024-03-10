import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Self

from .billing_cycle import BillingCycle
from .money import Money
from .worker import Worker


class TransactionType(StrEnum):
    ENROLL = "enroll"
    WITHDRAW = "withdraw"
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

    @classmethod
    def new(
        cls,
        worker: Worker,
        billing_cycle: BillingCycle,
        type: TransactionType,
        credit: Money,
        debit: Money,
        description: str,
    ) -> Self:
        return cls(
            public_id=str(uuid.uuid4()),
            worker=worker,
            billing_cycle=billing_cycle,
            type=type,
            credit=credit,
            debit=debit,
            description=description,
            created_at=datetime.utcnow(),
        )
