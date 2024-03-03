from pydantic import BaseModel, Field


class EmptyResponse(BaseModel):
    result: dict = Field(default_factory=dict)
