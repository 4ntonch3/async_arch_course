from schema_registry import SchemaRegistry

from domain import interfaces, usecases
from external import AuthServiceClient


auth_service_client: AuthServiceClient
schema_registry: SchemaRegistry
workers_repository: interfaces.WorkersRepository

add_task: usecases.AddTaskUsecase
complete_task: usecases.CompleteTaskUsecase
get_worker_tasks: usecases.GetWorkerTasksUsecase
reassign_tasks: usecases.ReassignTasksUsecase
