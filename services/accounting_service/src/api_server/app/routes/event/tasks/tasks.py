from api_server.app import dependency
from external import broker

from . import models


_CUD_TASKS_EVENT_TOPIC = "task-stream"
_BE_TASKS_EVENT_TOPIC = "task-lifecycle"


@broker.subscriber(_CUD_TASKS_EVENT_TOPIC)
async def handle_cud_task_event(event: dict) -> None:
    event_title = event.get("title")

    if event_title != models.TaskCreatedEvent.EVENT_TITLE:
        return

    task_created_event = models.TaskCreatedEvent.model_validate(event)
    task_data = task_created_event.payload

    task = await dependency.tasks_repository.add(task_data.task_id)

    await dependency.message_broker.produce_task_costs_set(task)


@broker.subscriber(_BE_TASKS_EVENT_TOPIC, batch=True)
async def handle_be_task_event(events: list[dict]) -> None:
    for event in events:
        event_title = event.get("title")

        match event_title:
            case models.TaskAssignedEvent.EVENT_TITLE:
                task_assigned_event = models.TaskAssignedEvent.model_validate(event)
                task_data = task_assigned_event.payload
                await dependency.apply_withdraw_transaction.execute(
                    task_data.task_id, task_data.new_assignee.id
                )
            case models.TaskClosedEvent.EVENT_TITLE:
                task_closed_event = models.TaskClosedEvent.model_validate(event)
                task_data = task_closed_event.payload
                await dependency.apply_enroll_transaction.execute(task_data.task_id, task_data.assignee.id)
            case _:
                continue
