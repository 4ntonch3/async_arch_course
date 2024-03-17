from schema_registry import EventType

from api_server.app import dependency
from domain import entities
from external import broker


_CUD_WORKERS_EVENT_TOPIC = "worker-stream"


@broker.subscriber(_CUD_WORKERS_EVENT_TOPIC)
async def handle_worker_created_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.WORKER_CREATED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]

    await dependency.workers_repository.add(
        event_payload["public_id"],
        event_payload["email"],
        entities.WorkerRole(event_payload["role"]),
    )
