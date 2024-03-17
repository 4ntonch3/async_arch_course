from domain import entities
from domain.interfaces import MessageBroker

from ..common import broker
from .event_builder import EventBuilder


class KafkaMessageBroker(MessageBroker):
    def __init__(self, event_builder: EventBuilder) -> None:
        self._event_builder = event_builder

        self._business_events_topic = "task-lifecycle"
        self._cud_events_topic = "task-stream"

    async def produce_task_added(self, task: entities.Task) -> None:
        task_added_event = self._event_builder.build_task_added_event(task)
        await broker.publish(task_added_event, self._business_events_topic)

    async def produce_task_created(self, task: entities.Task) -> None:
        task_created_event = self._event_builder.build_task_created_event(task)
        await broker.publish(task_created_event, self._cud_events_topic)

    async def produce_tasks_assigned(self, tasks: list[entities.Task]) -> None:
        await broker.publish_batch(
            *[self._event_builder.build_task_assigned_event(task) for task in tasks],
            topic=self._business_events_topic,
        )

    async def produce_task_completed(self, task: entities.Task) -> None:
        task_completed_event = self._event_builder.build_task_completed_event(task)
        await broker.publish(task_completed_event, self._business_events_topic)

    async def produce_task_closed(self, task: entities.Task) -> None:
        task_closed_event = self._event_builder.build_task_closed_event(task)
        await broker.publish(task_closed_event, self._cud_events_topic)
