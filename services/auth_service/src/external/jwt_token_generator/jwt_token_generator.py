import jwt

from domain import entities
from domain.interfaces import TokenGenerator

from .model import WorkerPayload


class JWTTokenGenerator(TokenGenerator):
    def __init__(self, secret: str, hash_algorithm: str = "HS256") -> None:
        self._secret = secret
        self._hash_algorithm = hash_algorithm

    def encode(self, worker: entities.Worker, token_lifetime_seconds: int) -> str:
        payload = WorkerPayload.from_domain(worker, token_lifetime_seconds)

        return jwt.encode(payload.to_dict(), key=self._secret, algorithm=self._hash_algorithm)

    def decode(self, token: str) -> entities.Worker:
        raw_payload = jwt.decode(token, self._secret, algorithms=[self._hash_algorithm])

        payload = WorkerPayload(**raw_payload)

        return payload.to_domain()
