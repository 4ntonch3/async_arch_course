from domain import entities
from domain.interfaces import TokenGenerator


class GetWorkerByTokenUsecase:
    def __init__(self, token_generator: TokenGenerator) -> None:
        self._token_generator = token_generator

    async def execute(self, token: str) -> entities.Worker:
        return self._token_generator.decode(token)
