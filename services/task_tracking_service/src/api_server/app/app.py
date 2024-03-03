from fastapi import FastAPI

from domain import usecases
from external import AuthServiceClient, broker

from . import dependency, routes


def create_web_app(
    auth_service_client: AuthServiceClient,
    add_task: usecases.AddTaskUsecase,
    add_worker: usecases.AddWorkerUsecase,
    close_task: usecases.CloseTaskUsecase,
    get_tasks_for_worker: usecases.GetTasksForWorkerUsecase,
    reassign_tasks: usecases.ReassignTasksUsecase,
) -> FastAPI:
    dependency.auth_service_client = auth_service_client
    dependency.add_task = add_task
    dependency.add_worker = add_worker
    dependency.close_task = close_task
    dependency.get_tasks_for_worker = get_tasks_for_worker
    dependency.reassign_tasks = reassign_tasks

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        on_startup=(broker.start,),
        on_shutdown=(broker.close,),
    )

    app.include_router(routes.task_router)

    return app
