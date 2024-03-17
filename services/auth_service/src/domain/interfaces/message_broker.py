import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_worker_created(self, worker: entities.Worker, email: str) -> None:
        pass
