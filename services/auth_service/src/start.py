import sys

from schema_registry import SchemaRegistry

import environment as env
from api_server import create_web_app, start_api_server
from domain import usecases
from external import EventBuilder, JWTTokenGenerator, KafkaMessageBroker, PostgresWorkersRepository
from logger import LOGGER


def main() -> int:
    try:
        token_generator = JWTTokenGenerator(env.JWT_SECRET)

        schema_registry = SchemaRegistry()
        event_builder = EventBuilder(schema_registry)
        message_broker = KafkaMessageBroker(event_builder)

        workers_repository = PostgresWorkersRepository(
            env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_PASSWORD, env.DB_TITLE
        )

        web_app = create_web_app(
            usecases.CreateTokenUsecase(workers_repository, token_generator, env.JWT_TOKEN_LIFETIME_SECONDS),
            usecases.RegisterWorkerUsecase(workers_repository, message_broker),
            usecases.GetWorkerByTokenUsecase(workers_repository, token_generator),
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
