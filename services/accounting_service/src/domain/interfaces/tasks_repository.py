import abc

from domain import entities


class TasksRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, public_id: str) -> entities.Task:
        pass

    @abc.abstractmethod
    async def get_by_public_id(self, public_id: str) -> entities.Task | None:
        pass
