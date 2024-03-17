import uuid
from datetime import UTC, datetime

from schema_registry import EventType, SchemaRegistry

from domain import entities


class EventBuilder:
    _PRODUCER_TITLE = "task_tracker"

    def __init__(self, schema_registry: SchemaRegistry) -> None:
        self._schema_registry = schema_registry

    def build_task_added_event(self, task: entities.Task) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskAdded",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.public_id,
                "assignee": {
                    "public_id": task.assignee.public_id,
                    "role": str(task.assignee.role),
                },
                "description": task.description,
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_ADDED, version)

        return event

    def build_task_assigned_event(self, task: entities.Task) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskAssigned",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.public_id,
                "assigned_worker_public_id": task.assignee.public_id,
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_ASSIGNED, version)

        return event

    def build_task_created_event(self, task: entities.Task) -> dict:
        version = "2"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskCreated",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.public_id,
                "assignee": {
                    "public_id": task.assignee.public_id,
                    "role": str(task.assignee.role),
                },
                "description": task.description,
                "jira_id": task.jira_id,
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_CREATED, version)

        return event

    def build_task_completed_event(self, task: entities.Task) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskCompleted",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.public_id,
                "assigned_worker_public_id": task.assignee.public_id,
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_COMPLETED, version)

        return event

    def build_task_closed_event(self, task: entities.Task) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskClosed",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.public_id,
                "assigned_worker_public_id": task.assignee.public_id,
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_CLOSED, version)

        return event

    def _generate_event_id(self) -> str:
        return str(uuid.uuid4())

    def _generate_time(self) -> str:
        return datetime.now(UTC).ctime()
