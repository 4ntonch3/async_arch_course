import abc

from domain import entities


class WorkersRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, worker: entities.Worker) -> None:
        pass

    @abc.abstractmethod
    async def get_random_with_developer_role(self) -> entities.Worker:
        pass
