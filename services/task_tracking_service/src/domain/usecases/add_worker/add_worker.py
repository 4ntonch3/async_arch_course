from domain import entities, interfaces


class AddWorkerUsecase:
    def __init__(self, workers_repository: interfaces.WorkersRepository) -> None:
        self._workers_repository = workers_repository

    async def execute(self, worker_id: str, role: str) -> None:
        new_worker = entities.Worker.new(worker_id, role)

        await self._workers_repository.add(new_worker)
