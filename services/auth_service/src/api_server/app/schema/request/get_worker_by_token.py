from pydantic import BaseModel

from ..object import Token


class GetWorkerByTokenRequestBody(BaseModel):
    token: Token
