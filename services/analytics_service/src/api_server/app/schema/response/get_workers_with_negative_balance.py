from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class Worker(BaseModel):
    id: StrictStr
    balance: StrictStr


class GetWorkersWithNegativeBalanceResponseBody(BaseModel):
    class GetWorkersWithNegativeBalanceResult(BaseModel):
        workers: list[Worker]

    result: GetWorkersWithNegativeBalanceResult

    @classmethod
    def from_domain(cls, workers: list[entities.Worker]) -> Self:
        return cls(
            result=cls.GetWorkersWithNegativeBalanceResult(
                workers=[Worker(id=worker.public_id, balance=str(worker.balance)) for worker in workers]
            )
        )
