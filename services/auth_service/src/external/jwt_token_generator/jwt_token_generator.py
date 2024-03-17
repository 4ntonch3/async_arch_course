import jwt

from domain import entities
from domain.interfaces import TokenGenerator

from .models import WorkerPayload


class JWTTokenGenerator(TokenGenerator):
    def __init__(self, secret: str) -> None:
        self._secret = secret
        self._hash_algorithm = "HS256"

    def encode(self, worker: entities.Worker, token_lifetime_seconds: int) -> str:
        payload = WorkerPayload.from_domain(worker, token_lifetime_seconds)

        return jwt.encode(payload.to_dict(), key=self._secret, algorithm=self._hash_algorithm)

    def decode_to_username(self, token: str) -> str:
        raw_payload = jwt.decode(token, self._secret, algorithms=[self._hash_algorithm])

        payload = WorkerPayload(**raw_payload)

        return payload.username
