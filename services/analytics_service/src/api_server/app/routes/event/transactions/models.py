from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from pydantic import BaseModel, StrictStr


class Event(BaseModel):
    title: StrictStr


class TransactionCreatedEvent(Event):
    class Payload(BaseModel):
        public_id: StrictStr
        worker_public_id: StrictStr
        type: StrictStr
        credit: Decimal
        debit: Decimal
        description: StrictStr
        created_at: datetime

    EVENT_TITLE: ClassVar[str] = "transaction_created"

    title: StrictStr = EVENT_TITLE
    payload: Payload
