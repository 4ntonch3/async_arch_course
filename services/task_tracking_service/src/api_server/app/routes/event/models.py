from typing import ClassVar

from pydantic import BaseModel, StrictStr


class Event(BaseModel):
    title: StrictStr
    payload: BaseModel


class WorkerCreatedEvent(Event):
    class Payload(BaseModel):
        worker_id: StrictStr
        username: StrictStr
        email: StrictStr
        role: StrictStr

    EVENT_TITLE: ClassVar[str] = "worker_created"

    title: StrictStr = EVENT_TITLE
    payload: Payload
