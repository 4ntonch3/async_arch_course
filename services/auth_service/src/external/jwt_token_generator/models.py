from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Self

from domain import entities


@dataclass
class WorkerPayload:
    username: str
    hashed_secret: str
    exp: datetime

    @classmethod
    def from_domain(cls, worker: entities.Worker, lifetime_seconds: int) -> Self:
        return cls(
            username=worker.username,
            hashed_secret=worker.hashed_secret,
            exp=datetime.now(UTC) + timedelta(seconds=lifetime_seconds),
        )

    def to_dict(self) -> dict:
        return asdict(self)
