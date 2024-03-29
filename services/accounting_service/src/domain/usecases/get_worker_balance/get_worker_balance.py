from domain import entities, interfaces


class GetWorkerBalanceUsecase:
    def __init__(self, workers_repository: interfaces.WorkersRepository) -> None:
        self._workers_repository = workers_repository

    async def execute(self, worker_public_id: str) -> entities.Money:
        worker = await self._workers_repository.get_by_public_id(worker_public_id)

        return worker.balance
