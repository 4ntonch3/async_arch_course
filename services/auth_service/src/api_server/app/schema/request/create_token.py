from pydantic import BaseModel, StrictStr


class CreateTokenRequestBody(BaseModel):
    username: StrictStr
    secret: StrictStr
