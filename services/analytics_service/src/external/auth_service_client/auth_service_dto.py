from typing import Self

from pydantic import BaseModel, StrictStr


class Worker(BaseModel):
    public_id: StrictStr
    role: StrictStr

    @classmethod
    def from_dict(cls, raw_worker: dict) -> Self:
        return cls.model_validate(raw_worker)
