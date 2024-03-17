from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from api_server.app import dependency, schema
from external import auth_service_dto


finances_router = APIRouter(prefix="/api/v1/finances", tags=["FINANCES"])


async def _get_worker(
    x_token: Annotated[str | None, Header()] = None,
) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@finances_router.get(
    path="/workers-with-negative-balance",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetWorkersWithNegativeBalanceResponseBody
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def get_workers_with_negative_balance(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role.lower() != "administrator":
        return schema.response.PermissionErrorResponse()

    workers_with_negative_balance = await dependency.get_workers_with_negative_balance.execute()

    return schema.response.GetWorkersWithNegativeBalanceResponseBody.from_domain(
        workers_with_negative_balance
    )


@finances_router.get(
    path="/today-managers-profit",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetTodaysManagerProfitResponseBody
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def get_todays_manager_profit(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role.lower() != "administrator":
        return schema.response.PermissionErrorResponse()

    profit = await dependency.get_todays_manager_profit.execute()

    return schema.response.GetTodaysManagerProfitResponseBody.from_money(profit)
