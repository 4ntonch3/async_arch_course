from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, StrictStr

from domain import entities


class TransactionType(StrEnum):
    INCOME = "income"
    DEBIT = "debit"
    PAYOUT = "payout"

    @classmethod
    def from_domain(cls, type: entities.TransactionType) -> Self:
        match type:
            case entities.TransactionType.ENROLL:
                return cls("income")
            case entities.TransactionType.WITHDRAW:
                return cls("debit")
            case entities.TransactionType.PAYMENT:
                return cls("payout")


class Transaction(BaseModel):
    id: StrictStr
    type: StrictStr
    income: StrictStr
    debit: StrictStr
    description: StrictStr
    done_at: datetime


class GetFinancialReportResponse(BaseModel):
    class GetFinancialReportResult(BaseModel):
        transactions: list[Transaction]

    result: GetFinancialReportResult

    @classmethod
    def from_transcations(cls, transactions: list[entities.Transaction]) -> Self:
        return cls(
            result=cls.GetFinancialReportResult(
                transactions=[
                    Transaction(
                        id=transaction.public_id,
                        type=TransactionType.from_domain(transaction.type),
                        income=str(transaction.debit),
                        debit=str(transaction.credit),
                        description=transaction.description,
                        done_at=transaction.created_at,
                    )
                    for transaction in transactions
                ]
            )
        )
