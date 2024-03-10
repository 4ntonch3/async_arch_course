from pydantic import BaseModel, Field, StrictInt, StrictStr


class EmptyResponse(BaseModel):
    result: dict = Field(default_factory=dict)


class UnauthorizedErrorResponse(BaseModel):
    class UnauthorizedErrorResult(BaseModel):
        code: StrictInt = 1
        message: StrictStr = "You are not authorized."

    error: UnauthorizedErrorResult = UnauthorizedErrorResult()


class PermissionErrorResponse(BaseModel):
    class PermissionErrorResult(BaseModel):
        code: StrictInt = 2
        message: StrictStr = "You don't have permissions for action."

    error: PermissionErrorResult = PermissionErrorResult()
