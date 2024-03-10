from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from api_server.app import dependency, schema
from external import auth_service_dto


developer_router = APIRouter(prefix="/api/v1/developer", tags=["DEVELOPER"])


async def _get_worker(x_token: Annotated[str | None, Header()] = None) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@developer_router.get(
    path="/balance",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetBalanceResponse
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def get_balance(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role != "developer":
        raise schema.response.PermissionErrorResponse()

    balance = await dependency.get_worker_balance.execute(worker.public_id)

    return schema.response.GetBalanceResponse.from_money(balance)


@developer_router.get(
    path="/financial-report",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetFinancialReportResponse
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def get_financial_report(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role != "developer":
        raise schema.response.PermissionErrorResponse()

    transactions = await dependency.get_worker_transactions.execute(worker.public_id)

    return schema.response.GetFinancialReportResponse.from_transcations(transactions)
