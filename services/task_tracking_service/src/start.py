import sys

import environment as env
from api_server import create_web_app, start_api_server
from domain import usecases
from external import (
    AuthServiceClient,
    KafkaMessageBroker,
    PostgresTasksRepository,
    PostgresWorkersRepository,
)
from logger import LOGGER


def main() -> int:
    try:
        message_broker = KafkaMessageBroker()
        tasks_repository = PostgresTasksRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        workers_repository = PostgresWorkersRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )

        web_app = create_web_app(
            AuthServiceClient(env.AUTH_SERVICE_HOST, env.AUTH_SERVICE_PORT),
            usecases.AddTaskUsecase(tasks_repository, workers_repository, message_broker),
            usecases.AddWorkerUsecase(workers_repository),
            usecases.CloseTaskUsecase(tasks_repository, message_broker),
            usecases.GetTasksForWorkerUsecase(tasks_repository),
            usecases.ReassignTasksUsecase(tasks_repository, workers_repository, message_broker),
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
