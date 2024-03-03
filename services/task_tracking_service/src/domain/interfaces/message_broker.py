import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_task_added(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_closed(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_reassigned(self, task: entities.Task) -> None:
        pass
