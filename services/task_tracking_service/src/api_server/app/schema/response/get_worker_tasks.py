from typing import Self

from pydantic import BaseModel

from domain import entities

from ..object import Task


class GetWorkerTasksResponse(BaseModel):
    class GetWorkerTasksResult(BaseModel):
        tasks: list[Task]

    result: GetWorkerTasksResult

    @classmethod
    def from_domain(cls, tasks: list[entities.Task]) -> Self:
        return cls(result=cls.GetWorkerTasksResult(tasks=[Task.from_domain(task) for task in tasks]))
