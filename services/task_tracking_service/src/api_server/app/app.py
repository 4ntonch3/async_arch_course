from fastapi import FastAPI
from schema_registry import SchemaRegistry

from domain import interfaces, usecases
from external import AuthServiceClient, broker

from . import dependency, routes


def create_web_app(
    auth_service_client: AuthServiceClient,
    schema_registry: SchemaRegistry,
    workers_repository: interfaces.WorkersRepository,
    add_task: usecases.AddTaskUsecase,
    complete_task: usecases.CompleteTaskUsecase,
    get_worker_tasks: usecases.GetWorkerTasksUsecase,
    reassign_tasks: usecases.ReassignTasksUsecase,
) -> FastAPI:
    dependency.auth_service_client = auth_service_client
    dependency.schema_registry = schema_registry
    dependency.workers_repository = workers_repository
    dependency.add_task = add_task
    dependency.complete_task = complete_task
    dependency.get_worker_tasks = get_worker_tasks
    dependency.reassign_tasks = reassign_tasks

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        on_startup=(broker.start,),
        on_shutdown=(broker.close,),
    )

    app.include_router(routes.tasks_router)

    return app
