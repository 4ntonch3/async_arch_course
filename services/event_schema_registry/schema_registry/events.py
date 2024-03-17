from enum import StrEnum, auto


class EventType(StrEnum):
    PAYOUT_DONE = auto()

    TASK_COST_CREATED = auto()

    TASK_ADDED = auto()
    TASK_ASSIGNED = auto()
    TASK_COMPLETED = auto()
    TASK_CREATED = auto()
    TASK_CLOSED = auto()
    TASK_UPDATED = auto()

    DEPOSIT_TRANSACTION_APPLIED = auto()
    PAYMENT_TRANSACTION_APPLIED = auto()
    WITHDRAWAL_TRANSACTION_APPLIED = auto()

    WORKER_CREATED = auto()
