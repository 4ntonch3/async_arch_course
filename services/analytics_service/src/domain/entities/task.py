from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .money import Money


class TaskStatus(StrEnum):
    OPENED = "opened"
    COMPLETED = "completed"


@dataclass
class TaskCost:
    id: str
    public_id: str
    assign_fee: Money
    completion_award: Money


@dataclass
class Task:
    id: str
    public_id: str
    status: TaskStatus
    cost: TaskCost | None
    created_at: datetime
    closed_at: datetime | None
