from domain.interfaces import TokenGenerator, WorkersRepository

from .common import hash_secret


class CreateTokenUsecase:
    def __init__(
        self,
        workers_repository: WorkersRepository,
        token_generator: TokenGenerator,
        token_lifetime_seconds: int,
    ) -> None:
        self._workers_repository = workers_repository
        self._token_generator = token_generator
        self._token_lifetime_seconds = token_lifetime_seconds

    async def execute(self, username: str, secret: str) -> str:
        worker = await self._workers_repository.get_by_username(username)

        if worker.hashed_secret != hash_secret(secret):
            msg_exc = "Invalid credentials."
            raise RuntimeError(msg_exc)  # TODO

        return self._token_generator.encode(worker, self._token_lifetime_seconds)
