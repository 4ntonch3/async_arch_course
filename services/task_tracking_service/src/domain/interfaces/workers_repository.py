import abc

from domain import entities


class WorkersRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, public_id: str, role: entities.WorkerRole) -> entities.Worker:
        pass
