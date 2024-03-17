from domain import entities
from domain.interfaces import TokenGenerator, WorkersRepository


class GetWorkerByTokenUsecase:
    def __init__(self, workers_repository: WorkersRepository, token_generator: TokenGenerator) -> None:
        self._workers_repository = workers_repository
        self._token_generator = token_generator

    async def execute(self, token: str) -> entities.Worker:
        username = self._token_generator.decode_to_username(token)

        return await self._workers_repository.get_by_username(username)
