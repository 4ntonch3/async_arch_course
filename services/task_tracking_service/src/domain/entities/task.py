from dataclasses import dataclass
from enum import StrEnum

from .worker import Worker


class TaskStatus(StrEnum):
    OPEN = "open"
    COMPLETED = "completed"


@dataclass
class Task:
    id: int
    public_id: str
    external_id: str
    jira_id: str | None
    assignee: Worker
    description: str
    status: TaskStatus

    def is_opened(self) -> bool:
        return self.status is TaskStatus.OPEN

    def reassign(self, new_assignee: Worker) -> None:
        self.assignee = new_assignee

    def close(self) -> None:
        if self.status is TaskStatus.COMPLETED:
            msg_exc = "Task is already closed."
            raise RuntimeError(msg_exc)  # TODO

        self.status = TaskStatus.COMPLETED
