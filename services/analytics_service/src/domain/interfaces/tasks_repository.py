import abc
from datetime import datetime

from domain import entities


class TasksRepository(abc.ABC):
    @abc.abstractmethod
    async def add(
        self,
        public_id: str,
        status: entities.TaskStatus,
        created_at: datetime,
        closed_at: datetime | None,
    ) -> entities.Task:
        pass

    @abc.abstractmethod
    async def set_cost(
        self,
        task_public_id: str,
        cost_public_id: str,
        assign_fee: entities.Money,
        completion_award: entities.Money,
    ) -> None:
        pass

    @abc.abstractmethod
    async def close(self, public_id: str) -> None:
        pass

    @abc.abstractmethod
    async def get_most_expensive(self, start_date: datetime, end_date: datetime) -> entities.Task:
        pass
