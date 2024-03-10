from decimal import Decimal
from typing import ClassVar

from pydantic import BaseModel, StrictStr

from domain import entities


class Event(BaseModel):
    title: StrictStr


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

    def to_domain(self) -> entities.Task:
        return entities.Task(
            id_=self.payload.task_id,
            status=entities.TaskStatus.OPENED,
            cost=None,
            closed_at=None,
        )


class TaskCostsSetEvent(Event):
    class Payload(BaseModel):
        public_id: StrictStr
        assign_fee: Decimal
        completion_award: Decimal

    EVENT_TITLE: ClassVar[str] = "task_costs_set"

    title: StrictStr = EVENT_TITLE
    payload: Payload


class TaskClosedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        assignee: Worker

    EVENT_TITLE: ClassVar[str] = "task_closed"

    title: StrictStr = EVENT_TITLE
    payload: Payload
