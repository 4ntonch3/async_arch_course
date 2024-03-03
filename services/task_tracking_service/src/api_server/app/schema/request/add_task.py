from pydantic import BaseModel, StrictStr


class AddTaskRequestBody(BaseModel):
    description: StrictStr
