from dataclasses import dataclass
from enum import StrEnum


class WorkerRole(StrEnum):
    ADMINISTATOR = "administrator"
    ACCOUNTANT = "accountant"
    DEVELOPER = "developer"
    MANAGER = "manager"


@dataclass
class Worker:
    id: str
    public_id: str
    role: WorkerRole
