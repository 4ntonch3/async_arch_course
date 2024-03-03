from typing import ClassVar, Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Event(BaseModel):
    title: StrictStr


class WorkerAddedEvent(Event):
    EVENT_TITLE: ClassVar[StrictStr] = "worker_added"

    title: StrictStr = EVENT_TITLE
    id: StrictStr
    username: StrictStr
    email: StrictStr
    role: StrictStr

    @classmethod
    def from_domain(cls, worker: entities.Worker) -> Self:
        return cls(
            id=worker.id_,
            username=worker.username,
            email=worker.email,
            role=str(worker.role),
        )
