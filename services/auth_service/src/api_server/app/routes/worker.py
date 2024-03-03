from fastapi import APIRouter, status

from .. import dependency, schema


worker_router = APIRouter(prefix="/api/v1/worker", tags=["WORKER"])


@worker_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.EmptyResponse}},
)
async def create_worker(body: schema.request.CreateWorkerRequestBody):
    await dependency.create_worker.execute(body.username, body.secret, body.email, body.role)

    return schema.response.EmptyResponse()
