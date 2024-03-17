from fastapi import APIRouter, status

from .. import dependency, schema


workers_router = APIRouter(prefix="/api/v1/workers", tags=["WORKERS"])


@workers_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.EmptyResponse}},
)
async def register_worker(body: schema.request.RegisterWorkerRequestBody):
    await dependency.register_worker.execute(body.username, body.secret, body.email, body.role)

    return schema.response.EmptyResponse()
