from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class GetTodaysManagerProfitResponseBody(BaseModel):
    class GetManagersDailyProfitResult(BaseModel):
        profit: StrictStr

    result: GetManagersDailyProfitResult

    @classmethod
    def from_money(cls, profit: entities.Money) -> Self:
        return cls(result=cls.GetManagersDailyProfitResult(profit=str(profit)))
