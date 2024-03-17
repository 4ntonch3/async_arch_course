from pydantic import BaseModel, StrictStr


class CompleteTaskRequestBody(BaseModel):
    task_id: StrictStr
