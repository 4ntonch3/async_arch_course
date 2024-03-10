from fastapi import APIRouter, status

from api_server.app import dependency, schema


billing_cycles_router = APIRouter(prefix="/api/v1/billing_cycles", tags=["BILLING_CYCLES"])


@billing_cycles_router.post(
    path="/close",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.EmptyResponse | schema.response.UnauthorizedErrorResponse
        }
    },
)
async def close_billing_cycles():
    await dependency.close_billing_cycles.execute()

    return schema.response.EmptyResponse()
