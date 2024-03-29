import abc
from datetime import datetime

from domain import entities


class TransactionsRepository(abc.ABC):
    @abc.abstractmethod
    async def add(
        self,
        public_id: str,
        worker_public_id: str,
        type: entities.TransactionType,
        value: entities.Money,
        created_at: datetime,
    ) -> None:
        pass

    @abc.abstractmethod
    async def get_todays_managers_profit(self) -> entities.Money:
        pass
