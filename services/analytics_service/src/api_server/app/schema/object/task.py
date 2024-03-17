from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Task(BaseModel):
    id: StrictStr
    cost: StrictStr

    @classmethod
    def from_domain(cls, task: entities.Task) -> Self:
        return cls(id=task.public_id, cost=str(task.cost.completion_award))
