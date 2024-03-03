from typing import Self

from pydantic import BaseModel, StrictStr


class AddTaskResponse(BaseModel):
    class CreateTaskResult(BaseModel):
        id: StrictStr

    result: CreateTaskResult

    @classmethod
    def from_id(cls, task_id: str) -> Self:
        return cls(result=cls.CreateTaskResult(id=task_id))
