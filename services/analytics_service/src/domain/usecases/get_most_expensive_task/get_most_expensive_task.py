from datetime import datetime

from domain import entities, interfaces


class GetMostExpensiveTaskUsecase:
    def __init__(self, tasks_repository: interfaces.TasksRepository) -> None:
        self._tasks_repository = tasks_repository

    async def execute(self, start_date: datetime, end_date: datetime) -> entities.Task:
        return await self._tasks_repository.get_most_expensive(start_date, end_date)
