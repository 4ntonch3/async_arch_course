import abc
from typing import AsyncIterator

from domain import entities


class TasksRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def get(self, task_id: str) -> entities.Task:
        pass

    @abc.abstractmethod
    async def get_all_for_worker(self, worker_id: str) -> list[entities.Task]:
        pass

    @abc.abstractmethod
    async def update(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def stream_opened(self) -> AsyncIterator[entities.Task]:
        pass
