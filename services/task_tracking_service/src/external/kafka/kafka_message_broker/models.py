from enum import StrEnum
from typing import ClassVar, Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Event(BaseModel):
    title: StrictStr


class Worker(BaseModel):
    id: StrictStr
    role: StrictStr


class TaskAddedEvent(Event):
    EVENT_TITLE: ClassVar[str] = "task_added"

    class Status(StrEnum):
        OPENED = "opened"
        CLOSED = "closed"

    title: StrictStr = EVENT_TITLE
    id: StrictStr
    assignee: Worker
    description: StrictStr
    status: StrictStr

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            id=task.id_,
            assignee=Worker(id=task.assignee.id_, role=str(task.assignee.role)),
            description=task.description,
            status=str(task.status),
        )


class TaskClosedEvent(Event):
    EVENT_TITLE: ClassVar[str] = "task_closed"

    title: StrictStr = EVENT_TITLE
    id: StrictStr
    assignee: Worker
    description: StrictStr

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            id=task.id_,
            assignee=Worker(id=task.assignee.id_, role=str(task.assignee.role)),
            description=task.description,
        )


class TaskReassignedEvent(Event):
    EVENT_TITLE: ClassVar[str] = "task_reassigned"

    class Worker(BaseModel):
        id: StrictStr
        role: StrictStr

    title: StrictStr = EVENT_TITLE
    id: StrictStr
    assignee: Worker
    description: StrictStr

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            id=task.id_,
            assignee=Worker(id=task.assignee.id_, role=str(task.assignee.role)),
            description=task.description,
        )
