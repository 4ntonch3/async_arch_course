from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Event(BaseModel):
    title: StrictStr
    payload: BaseModel


class TaskCostsSetEvent(Event):
    class Payload(BaseModel):
        public_id: StrictStr
        assign_fee: Decimal
        completion_award: Decimal

    EVENT_TITLE: ClassVar[str] = "task_costs_set"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            payload=cls.Payload(
                public_id=task.public_id,
                assign_fee=Decimal(task.assign_fee),
                completion_award=Decimal(task.completion_award),
            )
        )


class PaymentCreatedEvent(Event):
    class Payload(BaseModel):
        class Transaction(BaseModel):
            public_id: StrictStr
            worker_public_id: StrictStr
            type: StrictStr
            credit: Decimal
            debit: Decimal
            description: StrictStr
            created_at: datetime

        public_id: StrictStr
        transaction: Transaction

    EVENT_TITLE: ClassVar[str] = "payment_created"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, payment: entities.Payment) -> Self:
        return cls(
            payload=cls.Payload(
                public_id=payment.public_id,
                transaction=cls.Payload.Transaction(
                    public_id=payment.transaction.public_id,
                    worker_public_id=payment.transaction.worker.public_id,
                    type=str(payment.transaction.type),
                    credit=payment.transaction.credit,
                    debit=payment.transaction.debit,
                    description=payment.transaction.description,
                    created_at=payment.transaction.created_at,
                ),
            )
        )


class TransactionAppliedEvent(Event):
    class Payload(BaseModel):
        public_id: StrictStr
        worker_public_id: StrictStr
        type: StrictStr
        credit: Decimal
        debit: Decimal
        description: StrictStr
        created_at: datetime

    EVENT_TITLE: ClassVar[str] = "transaction_applied"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, transaction: entities.Transaction) -> Self:
        return cls(
            payload=cls.Payload(
                public_id=transaction.public_id,
                worker_public_id=transaction.worker.public_id,
                type=str(transaction.type),
                credit=transaction.credit,
                debit=transaction.debit,
                description=transaction.description,
                created_at=transaction.created_at,
            )
        )


class PaymentProcessedEvent(Event):
    class Payload(BaseModel):
        public_id: StrictStr

    EVENT_TITLE: ClassVar[str] = "payment_processed"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, payment: entities.Payment) -> Self:
        return cls(payload=cls.Payload(public_id=payment.public_id))
