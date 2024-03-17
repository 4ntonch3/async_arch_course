from faststream.kafka import KafkaBroker

import environment as env
from domain import entities
from domain.interfaces import MessageBroker

from .event_builder import EventBuilder


broker = KafkaBroker(f"{env.BROKER_HOST}:{env.BROKER_PORT}")


class KafkaMessageBroker(MessageBroker):
    def __init__(self, event_builder: EventBuilder) -> None:
        self._event_builder = event_builder

        self._cud_events_topic = "worker-stream"

    async def produce_worker_created(self, worker: entities.Worker, email: str) -> None:
        worker_created_event = self._event_builder.build_worker_created(worker, email)

        await broker.publish(worker_created_event, self._cud_events_topic)
