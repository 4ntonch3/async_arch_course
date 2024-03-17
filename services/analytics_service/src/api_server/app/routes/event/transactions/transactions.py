from datetime import datetime

from schema_registry import EventType

from api_server.app import dependency
from domain import entities

from ..common import broker_router


_BE_ENROLL_TRANSACTION_EVENT_TOPIC = "transactions-deposit"
_BE_WITHDRAW_TRANSACTION_EVENT_TOPIC = "transactions-withdrawal"
_BE_PAYMENT_TRANSACTION_EVENT_TOPIC = "transactions-payment"


@broker_router.subscriber(_BE_ENROLL_TRANSACTION_EVENT_TOPIC)
async def handle_deposit_transaction_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.DEPOSIT_TRANSACTION_APPLIED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]
    await dependency.transactions_repository.add(
        event_payload["public_id"],
        event_payload["worker_public_id"],
        entities.TransactionType.DEPOSIT,
        entities.Money(event_payload["debit"]),
        datetime.strptime(event_payload["created_at"], "%c"),
    )


@broker_router.subscriber(_BE_WITHDRAW_TRANSACTION_EVENT_TOPIC)
async def handle_withdrawal_transaction_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(
            event, EventType.WITHDRAWAL_TRANSACTION_APPLIED, version="1"
        )
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]
    await dependency.transactions_repository.add(
        event_payload["public_id"],
        event_payload["worker_public_id"],
        entities.TransactionType.WITHDRAWAL,
        entities.Money(event_payload["credit"]),
        datetime.strptime(event_payload["created_at"], "%c"),
    )


@broker_router.subscriber(_BE_PAYMENT_TRANSACTION_EVENT_TOPIC)
async def handle_payment_transaction_event(event: dict) -> None:
    try:
        dependency.schema_registry.validate_event(event, EventType.PAYMENT_TRANSACTION_APPLIED, version="1")
    except Exception:
        return  # TODO: add logging?

    event_payload = event["payload"]
    await dependency.transactions_repository.add(
        event_payload["public_id"],
        event_payload["worker_public_id"],
        entities.TransactionType.PAYMENT,
        entities.Money(event_payload["credit"]),
        datetime.strptime(event_payload["created_at"], "%c"),
    )
