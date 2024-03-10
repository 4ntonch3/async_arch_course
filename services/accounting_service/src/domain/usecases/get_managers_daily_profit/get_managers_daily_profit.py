from domain import entities, interfaces


class GetManagersDailyProfitUsecase:
    def __init__(self, transactions_repository: interfaces.TransactionsRepository) -> None:
        self._transactions_repository = transactions_repository

    async def execute(self) -> list[entities.Transaction]:
        return await self._transactions_repository.get_daily_enroll_and_withdraw_difference()
