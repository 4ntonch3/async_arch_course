from domain import entities, interfaces


class GetTasksForWorkerUsecase:
    def __init__(self, tasks_repository: interfaces.TasksRepository) -> None:
        self._tasks_repository = tasks_repository

    async def execute(self, worker_id: str) -> list[entities.Task]:
        return await self._tasks_repository.get_all_for_worker(worker_id)
