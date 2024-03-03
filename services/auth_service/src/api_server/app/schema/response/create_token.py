from typing import Self

from pydantic import BaseModel

from ..object import Token


class CreateTokenResponse(BaseModel):
    class CreateTokenResult(BaseModel):
        token: Token

    result: CreateTokenResult

    @classmethod
    def from_token(cls, token: str) -> Self:
        return cls(result=cls.CreateTokenResult(token=token))
