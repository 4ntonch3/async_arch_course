import json
from pathlib import Path
from typing import ClassVar

import jsonschema

from . import errors
from .events import EventType


class SchemaLoader:
    _EVENT_TYPE_TO_DIRECTORY: ClassVar[dict[EventType, str]] = {
        EventType.PAYOUT_DONE: "payouts/done",
        EventType.TASK_COST_CREATED: "task_costs/created",
        EventType.TASK_ADDED: "tasks/added",
        EventType.TASK_ASSIGNED: "tasks/assigned",
        EventType.TASK_COMPLETED: "tasks/completed",
        EventType.TASK_CREATED: "tasks/created",
        EventType.TASK_CLOSED: "tasks/closed",
        EventType.TASK_UPDATED: "tasks/updated",
        EventType.DEPOSIT_TRANSACTION_APPLIED: "transactions/deposit_applied",
        EventType.PAYMENT_TRANSACTION_APPLIED: "transactions/payment_applied",
        EventType.WITHDRAWAL_TRANSACTION_APPLIED: "transactions/withdrawal_applied",
        EventType.WORKER_CREATED: "workers/created",
    }

    def __init__(self, schema_root_folder: Path) -> None:
        self._schema_root_folder = schema_root_folder

    def get_schema_for_event(self, type_: EventType, event_version: str) -> dict:
        path_to_schema_file = (
            self._schema_root_folder / self._EVENT_TYPE_TO_DIRECTORY[type_] / f"{event_version}.json"
        )

        with path_to_schema_file.open(mode="r") as schema_file:
            return json.loads(schema_file.read())


class SchemaRegistry:
    def __init__(self) -> None:
        self._schema_loader = SchemaLoader(Path(__file__).parent / "schemas")

    def validate_event(self, data: dict, type_: EventType, version: str) -> None:
        event_schema = self._schema_loader.get_schema_for_event(type_, version)

        try:
            jsonschema.validate(data, event_schema)
        except Exception as exc:
            raise errors.InvalidSchemaError() from exc
