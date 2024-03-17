from http import HTTPStatus

import aiohttp

from .auth_service_dto import Worker


class AuthServiceClient:
    def __init__(self, host: str, port: int) -> None:
        self._auth_service = f"http://{host}:{port}"

    async def get_worker_by_token(self, token: str) -> Worker:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3)) as session:
            async with session.get(
                f"{self._auth_service}/api/v1/token/worker", json={"token": token}
            ) as resp:
                body = await resp.text()
                if resp.status != HTTPStatus.OK:
                    msg_exc = f"Unexpected response from AuthService. Code: {resp.status}. Body: {body}."
                    raise RuntimeError(msg_exc)

                result = await resp.json()

                return Worker.from_dict(result["result"])
