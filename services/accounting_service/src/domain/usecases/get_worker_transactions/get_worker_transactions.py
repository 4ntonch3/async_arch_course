from domain import entities, interfaces


class GetWorkerTransactionsUsecase:
    def __init__(self, transactions_repository: interfaces.TransactionsRepository) -> None:
        self._transactions_repository = transactions_repository

    async def execute(self, worker_public_id: str) -> list[entities.Transaction]:
        return await self._transactions_repository.get_all_for_worker(worker_public_id)
