from typing import ClassVar

from pydantic import BaseModel, StrictStr


class Event(BaseModel):
    title: StrictStr
    payload: BaseModel


class Worker(BaseModel):
    id: StrictStr
    role: StrictStr


class TaskCreatedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        assignee: Worker
        description: StrictStr

    EVENT_TITLE: ClassVar[str] = "task_created"

    title: StrictStr = EVENT_TITLE
    payload: Payload


class TaskClosedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        assignee: Worker

    EVENT_TITLE: ClassVar[str] = "task_closed"

    title: StrictStr = EVENT_TITLE
    payload: Payload


class TaskAssignedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        new_assignee: Worker

    EVENT_TITLE: ClassVar[str] = "task_assigned"

    title: StrictStr = EVENT_TITLE
    payload: Payload
