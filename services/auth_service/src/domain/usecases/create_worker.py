from domain import entities
from domain.interfaces import MessageBroker, WorkersRepository

from .common import hash_secret


class CreateWorkerUsecase:
    def __init__(self, workers_repository: WorkersRepository, message_broker: MessageBroker) -> None:
        self._message_broker = message_broker
        self._workers_repository = workers_repository

    async def execute(self, username: str, secret: str, email: str, role: str) -> None:
        worker = entities.Worker.new(username, hash_secret(secret), email, role)

        await self._workers_repository.add(worker)

        await self._message_broker.produce_worker_added(worker)
