from enum import StrEnum
from typing import Self

from domain import entities


class WorkerRole(StrEnum):
    ACCOUNTANT = "accountant"
    ADMINISTRATOR = "administrator"
    DEVELOPER = "developer"
    MANAGER = "manager"

    @classmethod
    def from_domain(cls, role: entities.WorkerRole) -> Self:
        return cls(str(role))
