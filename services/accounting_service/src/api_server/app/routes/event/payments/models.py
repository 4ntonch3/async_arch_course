from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from pydantic import BaseModel, StrictStr


class Event(BaseModel):
    title: StrictStr
    payload: BaseModel


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
