from pydantic import BaseModel, StrictStr


class RegisterWorkerRequestBody(BaseModel):
    username: StrictStr
    secret: StrictStr
    email: StrictStr
    role: StrictStr
