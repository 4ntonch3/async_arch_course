from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, status

from api_server.app import dependency, schema
from external import auth_service_dto


tasks_router = APIRouter(prefix="/api/v1/tasks", tags=["TASKS"])


async def _get_worker(x_token: Annotated[str | None, Header()] = None) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@tasks_router.get(
    path="/most-expensive",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.GetMostExpensiveTaskResponseBody}},
)
async def get_most_expensive_task(
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
    within_days: int = Query(),
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role.lower() != "administrator":
        return schema.response.PermissionErrorResponse()

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=within_days)
    most_expensive_task = await dependency.get_most_expensive_task.execute(start_date, end_date)

    return schema.response.GetMostExpensiveTaskResponseBody.from_domain(most_expensive_task)
