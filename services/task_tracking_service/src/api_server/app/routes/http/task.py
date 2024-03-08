from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from api_server.app import dependency, schema
from domain import entities
from external import auth_service_dto


task_router = APIRouter(prefix="/api/v1/tasks", tags=["TASK"])


async def _get_worker(x_token: Annotated[str | None, Header()] = None) -> auth_service_dto.Worker | None:
    try:
        return await dependency.auth_service_client.get_worker_by_token(x_token)
    except Exception:
        return None


@task_router.post(
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

    task_id = await dependency.add_task.execute(body.description)

    return schema.response.AddTaskResponse.from_id(task_id)


@task_router.post(
    path="/{task_id}/close",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.EmptyResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def close_task(
    body: schema.request.CloseTaskRequestBody,
    worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)],
):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    await dependency.close_task.execute(body.task_id)

    return schema.response.EmptyResponse()


@task_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.GetTasksForWorkerResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def get_tasks_for_worker(worker: Annotated[auth_service_dto.Worker | None, Depends(_get_worker)]):
    if worker is None:
        return schema.response.UnauthorizedErrorResponse()

    tasks_for_worker = await dependency.get_tasks_for_worker.execute(worker.public_id)

    return schema.response.GetTasksForWorkerResponse.from_domain(tasks_for_worker)


@task_router.post(
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
