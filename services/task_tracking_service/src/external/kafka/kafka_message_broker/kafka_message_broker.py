from domain import entities
from domain.interfaces import MessageBroker

from ..common import broker
from . import models


class KafkaMessageBroker(MessageBroker):
    def __init__(self) -> None:
        self._business_events_topic = "tasks"
        self._cud_events_topic = "tasks-stream"

    async def produce_task_added(self, task: entities.Task) -> None:
        task_added_event = models.TaskAddedEvent.from_domain(task)

        await broker.publish(task_added_event, self._business_events_topic)

        await broker.publish(task_added_event, self._cud_events_topic)

    async def produce_task_closed(self, task: entities.Task) -> None:
        task_closed_event = models.TaskClosedEvent.from_domain(task)

        await broker.publish(task_closed_event, self._business_events_topic)

        await broker.publish(task_closed_event, self._cud_events_topic)

    async def produce_task_reassigned(self, task: entities.Task) -> None:
        await broker.publish(models.TaskReassignedEvent.from_domain(task), self._business_events_topic)
