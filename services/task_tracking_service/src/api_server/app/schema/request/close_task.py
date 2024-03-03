from pydantic import BaseModel, StrictStr


class CloseTaskRequestBody(BaseModel):
    task_id: StrictStr
