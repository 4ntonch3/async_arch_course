from domain import entities, interfaces


class GetWorkersWithNegativeBalanceUsecase:
    def __init__(self, workers_repository: interfaces.WorkersRepository) -> None:
        self._workers_repository = workers_repository

    async def execute(self) -> list[entities.Worker]:
        return await self._workers_repository.get_workers_with_negative_balance()
