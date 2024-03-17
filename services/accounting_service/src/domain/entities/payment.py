from dataclasses import dataclass
from enum import StrEnum

from .billing_cycle import BillingCycle
from .transaction import Transaction


class PaymentStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    PROCESSED = "processed"


@dataclass
class Payment:
    id: str
    public_id: str
    billing_cycle: BillingCycle
    transaction: Transaction
    status: PaymentStatus

    def change_status_to_in_progress(self) -> None:
        self.status = PaymentStatus.IN_PROGRESS

    def change_status_to_processed(self) -> None:
        self.status = PaymentStatus.PROCESSED

    def change_status_to_failed(self) -> None:
        self.status = PaymentStatus.FAILED
