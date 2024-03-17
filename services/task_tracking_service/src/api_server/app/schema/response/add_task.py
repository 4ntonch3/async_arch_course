from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class AddTaskResponse(BaseModel):
    class CreateTaskResult(BaseModel):
        task_id: StrictStr

    result: CreateTaskResult

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(result=cls.CreateTaskResult(task_id=task.external_id))
