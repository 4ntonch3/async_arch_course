from dataclasses import dataclass
from enum import StrEnum
from typing import Self


class WorkerRole(StrEnum):
    ADMINISTATOR = "administrator"
    ACCOUNTANT = "accountant"
    DEVELOPER = "developer"
    MANAGER = "manager"


@dataclass
class Worker:
    id_: str
    role: WorkerRole

    @classmethod
    def new(cls, id_: str, role: str) -> Self:
        return cls(id_=id_, role=WorkerRole(role))
