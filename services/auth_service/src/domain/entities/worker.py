from dataclasses import dataclass
from enum import StrEnum


class WorkerRole(StrEnum):
    ACCOUNTANT = "accountant"
    ADMINISTRATOR = "administrator"
    DEVELOPER = "developer"
    MANAGER = "manager"


@dataclass
class Worker:
    id: str
    public_id: str
    username: str
    hashed_secret: str
    role: WorkerRole
