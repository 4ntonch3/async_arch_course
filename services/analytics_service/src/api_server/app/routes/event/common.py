from faststream.kafka.fastapi import KafkaRouter

import environment as env


broker_router = KafkaRouter(f"{env.BROKER_HOST}:{env.BROKER_PORT}")
