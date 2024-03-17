import abc

from domain import entities


class WorkersRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, public_id: str, email: str, role: entities.WorkerRole) -> entities.Worker:
        pass

    @abc.abstractmethod
    async def get_all(self) -> list[entities.Worker]:
        pass

    @abc.abstractmethod
    async def get_by_public_id(self, public_id: str) -> entities.Worker:
        pass
