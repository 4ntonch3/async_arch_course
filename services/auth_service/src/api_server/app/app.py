from fastapi import FastAPI

from domain import CreateTokenUsecase, GetWorkerByTokenUsecase, RegisterWorkerUsecase
from external import broker

from . import dependency, routes


def create_web_app(
    create_token: CreateTokenUsecase,
    register_worker: RegisterWorkerUsecase,
    get_worker_by_token: GetWorkerByTokenUsecase,
) -> FastAPI:
    dependency.create_token = create_token
    dependency.register_worker = register_worker
    dependency.get_worker_by_token = get_worker_by_token

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        on_startup=(broker.start,),
        on_shutdown=(broker.close,),
    )

    app.include_router(routes.token_router)
    app.include_router(routes.workers_router)

    return app
