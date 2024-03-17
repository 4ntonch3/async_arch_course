from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from api_server.app import dependency, schema
from domain import entities
from external import auth_service_dto


tasks_router = APIRouter(prefix="/api/v1/tasks", tags=["TASKS"])


async def _get_worker(x_token: Annotated[str | None, Header()] = None) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@tasks_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.AddTaskResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def add_task(
    body: schema.request.AddTaskRequestBody,
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    task = await dependency.add_task.execute(body.description)

    return schema.response.AddTaskResponse.from_domain(task)


@tasks_router.post(
    path="/{task_id}/complete",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.EmptyResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def complete_task(
    body: schema.request.CompleteTaskRequestBody,
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    await dependency.complete_task.execute(body.task_id)

    return schema.response.EmptyResponse()


@tasks_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetWorkerTasksResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def get_worker_tasks(worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)]):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    worker_tasks = await dependency.get_worker_tasks.execute(worker.public_id)

    return schema.response.GetWorkerTasksResponse.from_domain(worker_tasks)


@tasks_router.post(
    path="/reassign",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.EmptyResponse
            | schema.response.UnauthorizedErrorResponse
            | schema.response.PermissionErrorResponse
        }
    },
)
async def reassign_tasks(worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)]):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    if worker.role not in (entities.WorkerRole.ADMINISTATOR, entities.WorkerRole.MANAGER):
        return schema.response.PermissionErrorResponse()

    await dependency.reassign_tasks.execute()

    return schema.response.EmptyResponse()
