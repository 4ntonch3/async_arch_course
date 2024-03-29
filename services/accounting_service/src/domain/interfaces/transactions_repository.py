import abc

from domain import entities


class TransactionsRepository(abc.ABC):
    @abc.abstractmethod
    async def apply_deposit(
        self, worker_public_id: str, value: entities.Money, description: str
    ) -> entities.Transaction:
        pass

    @abc.abstractmethod
    async def apply_withdrawal(
        self, worker_public_id: str, value: entities.Money, description: str
    ) -> entities.Transaction:
        pass

    @abc.abstractmethod
    async def apply_payment(self, worker_public_id: str, description: str) -> entities.Payment | None:
        pass

    @abc.abstractmethod
    async def get_all_for_worker(self, worker_public_id: str) -> list[entities.Transaction]:
        pass

    @abc.abstractmethod
    async def get_daily_deposit_and_withdrawal_difference(self) -> entities.Money:
        pass
