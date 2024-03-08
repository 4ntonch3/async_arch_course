from domain import entities
from domain.interfaces import MessageBroker

from ..common import broker
from . import models


class KafkaMessageBroker(MessageBroker):
    def __init__(self) -> None:
        self._business_events_topic = "task-lifecycle"
        self._cud_events_topic = "task-stream"

    async def produce_task_added(self, task: entities.Task) -> None:
        task_assigned_event = models.TaskAssignedEvent.from_domain(task)
        await broker.publish(task_assigned_event, self._business_events_topic)

        task_created_event = models.TaskCreatedEvent.from_domain(task)
        await broker.publish(task_created_event, self._cud_events_topic)

    async def produce_task_closed(self, task: entities.Task) -> None:
        task_closed_event = models.TaskClosedEvent.from_domain(task)
        await broker.publish(task_closed_event, self._business_events_topic)
        await broker.publish(task_closed_event, self._cud_events_topic)

    async def produce_tasks_assigned(self, tasks: list[entities.Task]) -> None:
        await broker.publish_batch(
            *[models.TaskAssignedEvent.from_domain(task) for task in tasks],
            topic=self._business_events_topic,
        )
