from domain import entities
from domain.interfaces import MessageBroker, WorkersRepository

from .common import hash_secret


class RegisterWorkerUsecase:
    def __init__(self, workers_repository: WorkersRepository, message_broker: MessageBroker) -> None:
        self._message_broker = message_broker
        self._workers_repository = workers_repository

    async def execute(self, username: str, secret: str, email: str, role: str) -> None:
        worker = await self._workers_repository.add(username, hash_secret(secret), entities.WorkerRole(role))

        await self._message_broker.produce_worker_created(worker, email)
