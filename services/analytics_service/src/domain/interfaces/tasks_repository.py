import abc
from datetime import datetime

from domain import entities


class TasksRepository(abc.ABC):
    @abc.abstractmethod
    async def add(
        self,
        public_id: str,
        status: entities.TaskStatus,
        cost: entities.Money | None,
        created_at: datetime,
        closed_at: datetime | None,
    ) -> entities.Task:
        pass

    @abc.abstractmethod
    async def set_cost(self, public_id: str, cost: entities.Money) -> None:
        pass

    @abc.abstractmethod
    async def close(self, public_id: str) -> None:
        pass

    @abc.abstractmethod
    async def get_most_expensive(self, start_date: datetime, end_date: datetime) -> entities.Task:
        pass
