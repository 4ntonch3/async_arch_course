import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_worker_added(self, worker: entities.Worker) -> None:
        pass
