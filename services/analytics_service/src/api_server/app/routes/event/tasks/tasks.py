from datetime import UTC, datetime

from schema_registry import EventType

from api_server.app import dependency
from domain import entities

from ..common import broker_router


_BE_TASKS_EVENT_TOPIC = "task-lifecycle"


@broker_router.subscriber(_BE_TASKS_EVENT_TOPIC)
async def handle_task_event(event: dict) -> None:
    event_name = event.get("event_name")

    match event_name:
        case "TaskAdded":
            await _handle_task_added_event(event)
        case "TaskCompleted":
            await _handle_task_completed_event(event)
        case _:
            return


async def _handle_task_added_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_ADDED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    await dependency.tasks_repository.add(
        event_payload["public_id"],
        entities.TaskStatus.OPENED,
        created_at=datetime.now(UTC),
        closed_at=None,
    )


async def _handle_task_completed_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_COMPLETED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    await dependency.tasks_repository.close(event_payload["public_id"])
