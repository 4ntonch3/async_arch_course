from typing import Self

from pydantic import BaseModel

from domain import entities

from ..object import Task


class GetTasksForWorkerResponse(BaseModel):
    class GetTasksForWorkerResult(BaseModel):
        tasks: list[Task]

    result: GetTasksForWorkerResult

    @classmethod
    def from_domain(cls, tasks: list[entities.Task]) -> Self:
        return cls(result=cls.GetTasksForWorkerResult(tasks=[Task.from_domain(task) for task in tasks]))
