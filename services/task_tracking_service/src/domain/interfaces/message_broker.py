import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_tasks_assigned(self, tasks: list[entities.Task]) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_added(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_created(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_closed(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_task_completed(self, task: entities.Task) -> None:
        pass
