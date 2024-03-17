import sys

from schema_registry import SchemaRegistry

import environment as env
from api_server import create_web_app, start_api_server
from domain import usecases
from external import (
    AuthServiceClient,
    EventBuilder,
    KafkaMessageBroker,
    PostgresPaymentsRepository,
    PostgresTasksRepository,
    PostgresTransactionsRepository,
    PostgresWorkersRepository,
    StubBankClient,
    StubEmailClient,
)
from logger import LOGGER


def main() -> int:
    try:
        schema_registry = SchemaRegistry()
        event_builder = EventBuilder(schema_registry)
        message_broker = KafkaMessageBroker(event_builder)

        transactions_repository = PostgresTransactionsRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        payments_repository = PostgresPaymentsRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        tasks_repository = PostgresTasksRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )
        workers_repository = PostgresWorkersRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )

        bank_client = StubBankClient()
        email_client = StubEmailClient()

        web_app = create_web_app(
            AuthServiceClient(env.AUTH_SERVICE_HOST, env.AUTH_SERVICE_PORT),
            schema_registry,
            tasks_repository,
            workers_repository,
            message_broker,
            usecases.ApplyDepositTransactionUsecase(
                tasks_repository, transactions_repository, message_broker
            ),
            usecases.ApplyWithdrawalTransactionUsecase(
                tasks_repository, transactions_repository, message_broker
            ),
            usecases.CloseBillingCyclesUsecase(transactions_repository, workers_repository, message_broker),
            usecases.PayoutWorkerUsecase(payments_repository, message_broker, bank_client, email_client),
            usecases.GetWorkerBalanceUsecase(workers_repository),
            usecases.GetWorkerTransactionsUsecase(transactions_repository),
            usecases.GetManagersDailyProfitUsecase(transactions_repository),
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
