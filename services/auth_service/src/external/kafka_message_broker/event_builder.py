import uuid
from datetime import UTC, datetime

from schema_registry import EventType, SchemaRegistry

from domain import entities


class EventBuilder:
    _PRODUCER_TITLE = "auth_service"

    def __init__(self, schema_registry: SchemaRegistry) -> None:
        self._schema_registry = schema_registry

    def build_worker_created(self, worker: entities.Worker, worker_email: str) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "WorkerCreated",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": worker.public_id,
                "username": worker.username,
                "email": worker_email,
                "role": str(worker.role),
            },
        }

        self._schema_registry.validate_event(event, EventType.WORKER_CREATED, version)

        return event

    def _generate_event_id(self) -> str:
        return str(uuid.uuid4())

    def _generate_time(self) -> str:
        return datetime.now(UTC).ctime()
