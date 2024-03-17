import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_task_cost_created(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_deposit_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        pass

    @abc.abstractmethod
    async def produce_withdrawal_transactions_applied(
        self, transactions: list[entities.Transaction]
    ) -> None:
        pass

    @abc.abstractmethod
    async def produce_payment_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        pass

    @abc.abstractmethod
    async def produce_payout_done(self, payment: entities.Payment) -> None:
        pass
