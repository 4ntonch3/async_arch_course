from typing import ClassVar, Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Event(BaseModel):
    title: StrictStr


class WorkerCreatedEvent(Event):
    class Payload(BaseModel):
        worker_id: StrictStr
        username: StrictStr
        email: StrictStr
        role: StrictStr

    EVENT_TITLE: ClassVar[str] = "worker_created"

    title: StrictStr = EVENT_TITLE
    payload: Payload

    @classmethod
    def from_domain(cls, worker: entities.Worker) -> Self:
        return cls(
            payload=cls.Payload(
                worker_id=worker.public_id,
                username=worker.username,
                email=worker.email,
                role=str(worker.role),
            )
        )
