from api_server.app import dependency
from external import broker

from . import models


_BE_PAYMENTS_EVENT_TOPIC = "payment-lifecycle"


@broker.subscriber(_BE_PAYMENTS_EVENT_TOPIC, batch=True)
async def handle_transactions_event(events: list[dict]) -> None:
    for event in events:
        event_title = event.get("title")

        if event_title != models.PaymentCreatedEvent.EVENT_TITLE:
            continue

        payment_created_event = models.PaymentCreatedEvent.model_validate(event)

        await dependency.worker_payout.execute(payment_created_event.payload.public_id)
