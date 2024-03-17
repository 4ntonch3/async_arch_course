from domain import entities, interfaces


class GetTodaysManagerProfitUsecase:
    def __init__(self, transactions_repository: interfaces.TransactionsRepository) -> None:
        self._transactions_repository = transactions_repository

    async def execute(self) -> entities.Money:
        return await self._transactions_repository.get_todays_managers_profit()
