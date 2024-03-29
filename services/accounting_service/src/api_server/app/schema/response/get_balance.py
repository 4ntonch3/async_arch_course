from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class GetBalanceResponse(BaseModel):
    class GetBalanceResult(BaseModel):
        balance: StrictStr

    result: GetBalanceResult

    @classmethod
    def from_money(cls, balance: entities.Money) -> Self:
        return cls(result=cls.GetBalanceResult(balance=str(balance)))
