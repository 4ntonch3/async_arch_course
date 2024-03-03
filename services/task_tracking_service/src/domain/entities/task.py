import uuid
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from .worker import Worker


class TaskStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"


@dataclass
class Task:
    id_: str
    assignee: Worker
    description: str
    status: TaskStatus

    @classmethod
    def new(cls, description: str, assignee: Worker) -> Self:
        return cls(
            id_=str(uuid.uuid4()),
            assignee=assignee,
            description=description,
            status=TaskStatus.OPENED,
        )

    def is_opened(self) -> bool:
        return self.status is TaskStatus.OPENED

    def reassign(self, new_assignee: Worker) -> None:
        self.assignee = new_assignee

    def close(self) -> None:
        if self.status is TaskStatus.CLOSED:
            msg_exc = "Task is already closed."
            raise RuntimeError(msg_exc)  # TODO

        self.status = TaskStatus.CLOSED
