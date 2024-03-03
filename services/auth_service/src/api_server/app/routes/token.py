from fastapi import APIRouter, status

from .. import dependency, schema


token_router = APIRouter(prefix="/api/v1/token", tags=["TOKEN"])


@token_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.create_token.CreateTokenResponse}},
)
async def create_token(body: schema.request.CreateTokenRequestBody):
    token = await dependency.create_token.execute(body.username, body.secret)

    return schema.response.create_token.CreateTokenResponse.from_token(token)


@token_router.post(
    path="/worker",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": schema.response.get_user_by_token.GetWorkerByTokenResponse}},
)
async def get_worker_by_token(body: schema.request.GetWorkerByTokenRequestBody):
    worker = await dependency.get_worker_by_token.execute(body.token)

    return schema.response.get_user_by_token.GetWorkerByTokenResponse.from_domain(worker)
