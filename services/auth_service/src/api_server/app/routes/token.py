from fastapi import APIRouter, status

from .. import dependency, schema


token_router = APIRouter(prefix="/api/v1/token", tags=["TOKEN"])


@token_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.CreateTokenResponse}},
)
async def create_token(body: schema.request.CreateTokenRequestBody):
    token = await dependency.create_token.execute(body.username, body.secret)

    return schema.response.CreateTokenResponse.from_token(token)


@token_router.get(
    path="/worker",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.GetWorkerByTokenResponse}},
)
async def get_worker_by_token(body: schema.request.GetWorkerByTokenRequestBody):
    worker = await dependency.get_worker_by_token.execute(body.token)

    return schema.response.GetWorkerByTokenResponse.from_domain(worker)
