from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .money import Money


class TaskStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"


@dataclass
class Task:
    id: str
    public_id: str
    status: TaskStatus
    cost: Money | None
    created_at: datetime
    closed_at: datetime | None
