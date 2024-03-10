from fastapi import FastAPI

from domain import interfaces, usecases
from external import AuthServiceClient

from . import dependency, routes


def create_web_app(
    auth_service_client: AuthServiceClient,
    tasks_repository: interfaces.TasksRepository,
    transactions_repository: interfaces.TransactionsRepository,
    workers_repository: interfaces.WorkersRepository,
    get_most_expensive_task: usecases.GetMostExpensiveTaskUsecase,
    get_workers_with_negative_balance: usecases.GetWorkersWithNegativeBalanceUsecase,
    get_todays_manager_profit: usecases.GetTodaysManagerProfitUsecase,
) -> FastAPI:
    dependency.auth_service_client = auth_service_client

    dependency.tasks_repository = tasks_repository
    dependency.transactions_repository = transactions_repository
    dependency.workers_repository = workers_repository

    dependency.get_most_expensive_task = get_most_expensive_task
    dependency.get_workers_with_negative_balance = get_workers_with_negative_balance
    dependency.get_todays_manager_profit = get_todays_manager_profit

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        lifespan=routes.broker_router.lifespan_context,
    )

    app.include_router(routes.broker_router)
    app.include_router(routes.tasks_router)
    app.include_router(routes.finances_router)

    return app
