from domain import usecases
from external import AuthServiceClient


auth_service_client: AuthServiceClient

add_task: usecases.AddTaskUsecase
add_worker: usecases.AddWorkerUsecase
close_task: usecases.CloseTaskUsecase
get_tasks_for_worker: usecases.GetTasksForWorkerUsecase
reassign_tasks: usecases.ReassignTasksUsecase
