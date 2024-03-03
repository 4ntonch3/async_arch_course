import uuid
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Self


class WorkerRole(StrEnum):
    ACCOUNTANT = "accountant"
    ADMINISTRATOR = "administrator"
    DEVELOPER = "developer"
    MANAGER = "manager"


@dataclass
class Worker:
    id_: str
    username: str
    secret: str
    email: str
    role: WorkerRole

    @classmethod
    def new(cls, username: str, secret: str, email: str, role: str) -> Self:
        return cls(
            id_=str(uuid.uuid4()),
            username=username,
            secret=secret,
            email=email,
            role=WorkerRole(role),
        )

    def to_dict(self) -> dict:
        return asdict(self)
