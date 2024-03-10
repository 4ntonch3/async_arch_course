import abc

from domain import entities


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def produce_task_costs_set(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def produce_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        pass

    @abc.abstractmethod
    async def produce_payments_created(self, payments: list[entities.Payment]) -> None:
        pass

    @abc.abstractmethod
    async def produce_payment_processed(self, payment: entities.Payment) -> None:
        pass
