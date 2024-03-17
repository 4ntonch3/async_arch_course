import abc

from domain import entities


class WorkersRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, username: str, secret_hash: str, role: entities.WorkerRole) -> entities.Worker:
        pass

    @abc.abstractmethod
    async def get_by_username(self, username: str) -> entities.Worker:
        pass
