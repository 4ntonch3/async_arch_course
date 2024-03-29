from schema_registry import EventType

from api_server.app import dependency
from external import broker


_CUD_TASKS_EVENT_TOPIC = "task-stream"
_BE_TASKS_EVENT_TOPIC = "task-lifecycle"


@broker.subscriber(_CUD_TASKS_EVENT_TOPIC)
async def handle_task_created_event(event: dict) -> None:
    if event.get("event_name") != "TaskCreated":
        return

    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_CREATED, version="2")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    task = await dependency.tasks_repository.add(event_payload["public_id"])

    await dependency.message_broker.produce_task_cost_created(task)


@broker.subscriber(_BE_TASKS_EVENT_TOPIC, batch=True)
async def handle_task_business_events(events: list[dict]) -> None:
    for event in events:
        event_title = event.get("event_name")

        # TODO: add batch processing & events producing
        match event_title:
            case "TaskAdded":
                await _handle_task_added_event(event)
            case "TaskAssigned":
                await _handle_task_assigned_event(event)
            case "TaskCompleted":
                await _handle_task_completed_event(event)
            case _:
                continue


async def _handle_task_added_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_ADDED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    description = f"Fee for being assigned to new task. Task ID: {event_payload['public_id']}."
    await dependency.apply_deposit_transaction.execute(
        event_payload["public_id"], event_payload["assignee"]["public_id"], description
    )


async def _handle_task_assigned_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_ASSIGNED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    description = f"Fee for being assigned to task. Task ID: {event_payload['public_id']}."
    await dependency.apply_deposit_transaction.execute(
        event_payload["public_id"], event_payload["assigned_worker_public_id"], description
    )


async def _handle_task_completed_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.TASK_COMPLETED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    description = f"Award for completing the task. Task ID: {event_payload['public_id']}"
    await dependency.apply_withdrawal_transaction.execute(
        event_payload["public_id"], event_payload["assigned_worker_public_id"], description
    )
