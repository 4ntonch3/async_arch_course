from api_server.app import dependency
from domain import entities

from ..common import broker_router
from . import models


_CUD_TRANSACTION_EVENT_TOPIC = "transaction-stream"


@broker_router.subscriber(_CUD_TRANSACTION_EVENT_TOPIC)
async def handle_transaction_event(event: dict) -> None:
    event_title = event.get("title", "")

    if event_title != models.TransactionCreatedEvent.EVENT_TITLE:
        return

    transaction_created_event = models.TransactionCreatedEvent.model_validate(event)
    transaction_data = transaction_created_event.payload

    match transaction_data.type:
        case "enroll":
            await dependency.transactions_repository.add(
                transaction_data.public_id,
                transaction_data.worker_public_id,
                entities.TransactionType.INCOME,
                value=transaction_data.debit,
                created_at=transaction_data.created_at,
            )
        case "withdraw":
            await dependency.transactions_repository.add(
                transaction_data.public_id,
                transaction_data.worker_public_id,
                entities.TransactionType.DEBIT,
                value=transaction_data.credit,
                created_at=transaction_data.created_at,
            )
        case "payment":
            await dependency.transactions_repository.add(
                transaction_data.public_id,
                transaction_data.worker_public_id,
                entities.TransactionType.PAYOUT,
                value=transaction_data.debit,
                created_at=transaction_data.created_at,
            )
