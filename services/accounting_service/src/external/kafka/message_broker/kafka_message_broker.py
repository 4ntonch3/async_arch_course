from domain import entities
from domain.interfaces import MessageBroker

from ..common import broker
from . import models


class KafkaMessageBroker(MessageBroker):
    def __init__(self) -> None:
        self._transaction_business_events_topic = "transactions"
        self._payments_business_events_topic = "payment-lifecycle"
        self._task_cud_events_topic = "task-stream"
        self._transaction_cud_events_topic = "transaction-stream"

    async def produce_task_costs_set(self, task: entities.Task) -> None:
        await broker.publish(
            models.TaskCostsSetEvent.from_domain(task),
            topic=self._task_cud_events_topic,
        )

    async def produce_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        await broker.publish_batch(
            *[models.TransactionAppliedEvent.from_domain(transaction) for transaction in transactions],
            topic=self._transaction_business_events_topic,
        )

        await broker.publish_batch(
            *[models.TransactionCreatedEvent.from_domain(transaction) for transaction in transactions],
            topic=self._transaction_cud_events_topic,
        )

    async def produce_payments_created(self, payments: list[entities.Payment]) -> None:
        await broker.publish_batch(
            *[models.PaymentCreatedEvent.from_domain(payment) for payment in payments],
            topic=self._payments_business_events_topic,
        )

        await broker.publish_batch(
            *[models.TransactionCreatedEvent.from_domain(payment.transaction) for payment in payments],
            topic=self._transaction_cud_events_topic,
        )

    async def produce_payment_processed(self, payment: entities.Payment) -> None:
        await broker.publish(
            models.PaymentProcessedEvent.from_domain(payment),
            topic=self._payments_business_events_topic,
        )
