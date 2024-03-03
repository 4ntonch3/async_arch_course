from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Self

from domain import entities


@dataclass
class WorkerPayload:
    public_id: str
    username: str
    secret: str
    email: str
    role: str
    exp: datetime

    @classmethod
    def from_domain(cls, worker: entities.Worker, lifetime_seconds: int) -> Self:
        return cls(
            public_id=worker.id_,
            username=worker.username,
            secret=worker.secret,
            email=worker.email,
            role=str(worker.role),
            exp=datetime.utcnow() + timedelta(seconds=lifetime_seconds),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_domain(self) -> entities.Worker:
        return entities.Worker(
            id_=self.public_id,
            username=self.username,
            secret=self.secret,
            email=self.email,
            role=entities.WorkerRole(self.role),
        )
