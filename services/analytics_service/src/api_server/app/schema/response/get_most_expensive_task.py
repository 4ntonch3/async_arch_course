from typing import Self

from pydantic import BaseModel

from domain import entities

from ..object import Task


class GetMostExpensiveTaskResponseBody(BaseModel):
    class GetMostExpensiveTaskResult(BaseModel):
        task: Task

    result: GetMostExpensiveTaskResult

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(result=cls.GetMostExpensiveTaskResult(task=Task.from_domain(task)))
