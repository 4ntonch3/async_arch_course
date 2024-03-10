from dataclasses import dataclass
from enum import StrEnum

from .money import Money


class WorkerRole(StrEnum):
    ADMINISTATOR = "administrator"
    ACCOUNTANT = "accountant"
    DEVELOPER = "developer"
    MANAGER = "manager"


@dataclass
class Worker:
    id: str
    public_id: str
    balance: Money
    role: WorkerRole
