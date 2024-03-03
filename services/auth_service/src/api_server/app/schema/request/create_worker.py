from pydantic import BaseModel, StrictStr


class CreateWorkerRequestBody(BaseModel):
    username: StrictStr
    secret: StrictStr
    email: StrictStr
    role: StrictStr
