import sys

from schema_registry import SchemaRegistry

import environment as env
from api_server import create_web_app, start_api_server
from domain import usecases
from external import (
    AuthServiceClient,
    PostgresTasksRepository,
    PostgresTransactionsRepository,
    PostgresWorkersRepository,
)
from logger import LOGGER


def main() -> int:
    try:
        schema_registry = SchemaRegistry()

        tasks_repository = PostgresTasksRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        transactions_repository = PostgresTransactionsRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        workers_repository = PostgresWorkersRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        web_app = create_web_app(
            AuthServiceClient(env.AUTH_SERVICE_HOST, env.AUTH_SERVICE_PORT),
            schema_registry,
            tasks_repository,
            transactions_repository,
            workers_repository,
            usecases.GetMostExpensiveTaskUsecase(tasks_repository),
            usecases.GetWorkersWithNegativeBalanceUsecase(workers_repository),
            usecases.GetTodaysManagerProfitUsecase(transactions_repository),
        )
    except Exception:
        LOGGER.critical("Can't initialize service.", exc_info=True)
        return -1

    try:
        start_api_server(web_app, host="0.0.0.0", port=env.SERVE_PORT)
    except Exception:
        LOGGER.critical("Critical error during process.", exc_info=True)
        return -1


if __name__ == "__main__":
    sys.exit(main())
