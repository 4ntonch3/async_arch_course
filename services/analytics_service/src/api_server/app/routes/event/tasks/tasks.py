from datetime import datetime

from api_server.app import dependency
from domain import entities

from ..common import broker_router
from . import models


_CUD_TASKS_EVENT_TOPIC = "task-stream"


@broker_router.subscriber(_CUD_TASKS_EVENT_TOPIC)
async def handle_task_event(event: dict) -> None:
    event_title = event.get("title", "")

    match event_title:
        case models.TaskCreatedEvent.EVENT_TITLE:
            task_created_event = models.TaskCreatedEvent.model_validate(event)
            task_data = task_created_event.payload
            await dependency.tasks_repository.add(
                task_data.task_id,
                entities.TaskStatus.OPENED,
                cost=None,
                created_at=datetime.utcnow(),
                closed_at=None,
            )
        case models.TaskCostsSetEvent.EVENT_TITLE:
            task_costs_set_event = models.TaskCostsSetEvent.model_validate(event)
            await dependency.tasks_repository.set_cost(
                task_costs_set_event.payload.public_id, task_costs_set_event.payload.completion_award
            )
        case models.TaskClosedEvent.EVENT_TITLE:
            task_closed_event = models.TaskClosedEvent.model_validate(event)
            await dependency.tasks_repository.close(task_closed_event.payload.task_id)
        case _:
            return
