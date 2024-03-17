import abc

from domain import entities


class TasksRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, jira_id: str | None, description: str) -> entities.Task:
        pass

    @abc.abstractmethod
    async def complete(self, external_id: str) -> entities.Task:
        pass

    @abc.abstractmethod
    async def get_all_for_worker(self, worker_public_id: str) -> list[entities.Task]:
        pass

    @abc.abstractmethod
    async def reassign_all_open(self) -> list[entities.Task]:
        pass
