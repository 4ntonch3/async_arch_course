from typing import ClassVar, Self

from pydantic import BaseModel, StrictStr

from domain import entities


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

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            payload=cls.Payload(
                task_id=task.public_id,
                assignee=Worker(id=task.assignee.id_, role=str(task.assignee.role)),
                description=task.description,
            )
        )


class TaskClosedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        assignee: Worker

    EVENT_TITLE: ClassVar[str] = "task_closed"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            payload=cls.Payload(
                task_id=task.public_id,
                assignee=Worker(
                    id=task.assignee.id_,
                    role=str(task.assignee.role),
                ),
            )
        )


class TaskAssignedEvent(Event):
    class Payload(BaseModel):
        task_id: StrictStr
        new_assignee: Worker

    EVENT_TITLE: ClassVar[str] = "task_assigned"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(
            payload=cls.Payload(
                task_id=task.public_id,
                new_assignee=Worker(
                    id=task.assignee.id_,
                    role=str(task.assignee.role),
                ),
            )
        )
