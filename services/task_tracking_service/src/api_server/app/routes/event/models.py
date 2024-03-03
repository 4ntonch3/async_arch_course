from typing import ClassVar

from pydantic import BaseModel, StrictStr


class Event(BaseModel):
    title: StrictStr


class WorkerAddedEvent(Event):
    EVENT_TITLE: ClassVar[str] = "worker_added"

    title: StrictStr = EVENT_TITLE
    id: StrictStr
    username: StrictStr
    email: StrictStr
    role: StrictStr
