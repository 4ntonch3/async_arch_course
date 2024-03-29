import abc

from domain import entities


class PaymentsRepository(abc.ABC):
    @abc.abstractmethod
    async def get_for_processing(self, payment_public_id: str) -> entities.Payment:
        pass

    @abc.abstractmethod
    async def mark_failed(self, payment_id: str) -> entities.Payment:
        pass

    @abc.abstractmethod
    async def mark_processed(self, payment_id: str) -> entities.Payment:
        pass
