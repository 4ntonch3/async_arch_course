from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities

from ..object import WorkerRole


class GetWorkerByTokenResponse(BaseModel):
    class GetWorkerByTokenResult(BaseModel):
        public_id: StrictStr
        role: WorkerRole

    result: GetWorkerByTokenResult

    @classmethod
    def from_domain(cls, worker: entities.Worker) -> Self:
        return cls(
            result=cls.GetWorkerByTokenResult(
                public_id=worker.public_id,
                role=WorkerRole.from_domain(worker.role),
            )
        )
