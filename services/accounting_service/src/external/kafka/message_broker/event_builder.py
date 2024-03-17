import uuid
from datetime import UTC, datetime

from schema_registry import EventType, SchemaRegistry

from domain import entities


class EventBuilder:
    _PRODUCER_TITLE = "task_tracker"

    def __init__(self, schema_registry: SchemaRegistry) -> None:
        self._schema_registry = schema_registry

    def build_enroll_transaction_applied_event(self, transaction: entities.Transaction) -> dict:
        if transaction.type is not entities.TransactionType.DEPOSIT:
            msg_exc = "Wrong type of transaction"
            raise RuntimeError(msg_exc)  # TODO

        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "DepositTransactionApplied",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": transaction.public_id,
                "worker_public_id": transaction.worker.public_id,
                "credit": str(transaction.credit),
                "debit": str(transaction.debit),
                "description": transaction.description,
                "created_at": transaction.created_at.ctime(),
            },
        }

        self._schema_registry.validate_event(event, EventType.DEPOSIT_TRANSACTION_APPLIED, version)

        return event

    def build_withdraw_transaction_applied_event(self, transaction: entities.Transaction) -> dict:
        if transaction.type is not entities.TransactionType.WITHDRAWAL:
            msg_exc = "Wrong type of transaction"
            raise RuntimeError(msg_exc)  # TODO

        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "WithdrawalTransactionApplied",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": transaction.public_id,
                "worker_public_id": transaction.worker.public_id,
                "credit": str(transaction.credit),
                "debit": str(transaction.debit),
                "description": transaction.description,
                "created_at": transaction.created_at.ctime(),
            },
        }

        self._schema_registry.validate_event(event, EventType.WITHDRAWAL_TRANSACTION_APPLIED, version)

        return event

    def build_payment_transaction_applied_event(self, transaction: entities.Transaction) -> dict:
        if transaction.type is not entities.TransactionType.PAYMENT:
            msg_exc = "Wrong type of transaction"
            raise RuntimeError(msg_exc)  # TODO

        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "PaymentTransactionApplied",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": transaction.public_id,
                "worker_public_id": transaction.worker.public_id,
                "credit": str(transaction.credit),
                "debit": str(transaction.debit),
                "description": transaction.description,
                "created_at": transaction.created_at.ctime(),
            },
        }

        self._schema_registry.validate_event(event, EventType.PAYMENT_TRANSACTION_APPLIED, version)

        return event

    def build_payout_done_event(self, payment: entities.Payment) -> dict:
        if payment.status is not entities.PaymentStatus.PROCESSED:
            msg_exc = "Payment is not processed yet."
            raise RuntimeError(msg_exc)  # TODO

        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "PayoutDone",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": payment.public_id,
                "worker_public_id": payment.transaction.worker.public_id,
                "money": str(payment.transaction.debit),
            },
        }

        self._schema_registry.validate_event(event, EventType.PAYOUT_DONE, version)

        return event

    def build_task_cost_created_event(self, task: entities.Task) -> dict:
        version = "1"
        event = {
            "event_id": self._generate_event_id(),
            "event_version": version,
            "event_name": "TaskCostCreated",
            "event_time": self._generate_time(),
            "producer": self._PRODUCER_TITLE,
            "payload": {
                "public_id": task.cost.public_id,
                "task_public_id": task.public_id,
                "assign_fee": str(task.cost.assign_fee),
                "completion_award": str(task.cost.completion_award),
            },
        }

        self._schema_registry.validate_event(event, EventType.TASK_COST_CREATED, version)

        return event

    def _generate_event_id(self) -> str:
        return str(uuid.uuid4())

    def _generate_time(self) -> str:
        return datetime.now(UTC).ctime()
