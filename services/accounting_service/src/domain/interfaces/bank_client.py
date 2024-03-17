import abc

from domain import entities


class BankClient(abc.ABC):
    @abc.abstractmethod
    async def transfer(self, worker_public_id: str, value: entities.Money) -> None:
        pass
