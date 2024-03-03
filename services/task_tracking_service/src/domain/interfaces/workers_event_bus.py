import abc

from domain import entities


class WorkersEventBus(abc.ABC):
    @abc.abstractmethod
    async def consume_worker_added(self) -> entities.Worker:
        pass
