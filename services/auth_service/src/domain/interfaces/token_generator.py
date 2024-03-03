import abc

from domain import entities


class TokenGenerator(abc.ABC):
    @abc.abstractmethod
    def encode(self, worker: entities.Worker, token_lifetime_seconds: int) -> str:
        pass

    @abc.abstractmethod
    def decode(self, token: str) -> entities.Worker:
        pass
