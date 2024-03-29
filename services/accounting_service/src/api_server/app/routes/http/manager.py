from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from api_server.app import dependency, schema
from external import auth_service_dto


manager_router = APIRouter(prefix="/api/v1/manager", tags=["MANAGER"])


async def _get_worker(x_token: Annotated[str | None, Header()] = None) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@manager_router.get(
    path="/daily-profit",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetManagersDailyProfitResponse
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def get_daily_profit(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role not in ("manager", "administrator"):
        raise schema.response.PermissionErrorResponse()

    profit = await dependency.get_managers_daily_profit.execute()

    return schema.response.GetManagersDailyProfitResponse.from_money(profit)
