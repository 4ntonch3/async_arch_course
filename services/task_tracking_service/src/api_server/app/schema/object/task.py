from enum import StrEnum
from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class TaskStatus(StrEnum):
    OPEN = "open"
    COMPLETED = "completed"


class Task(BaseModel):
    id: StrictStr
    description: str
    status: TaskStatus

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(id=task.external_id, description=task.description, status=TaskStatus(str(task.status)))
