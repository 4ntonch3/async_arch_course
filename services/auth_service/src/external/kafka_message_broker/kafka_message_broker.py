from faststream.kafka import KafkaBroker

import environment as env
from domain import entities
from domain.interfaces import MessageBroker

from . import models


broker = KafkaBroker(f"{env.BROKER_HOST}:{env.BROKER_PORT}")


class KafkaMessageBroker(MessageBroker):
    def __init__(self) -> None:
        self._cud_events_topic = "workers-stream"

    async def produce_worker_added(self, worker: entities.Worker) -> None:
        worker_added_event = models.WorkerAddedEvent.from_domain(worker)

        await broker.publish(worker_added_event, self._cud_events_topic)
