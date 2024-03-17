from domain import entities
from domain.interfaces import MessageBroker

from ..common import broker
from .event_builder import EventBuilder


class KafkaMessageBroker(MessageBroker):
    def __init__(self, event_builder: EventBuilder) -> None:
        self._event_builder = event_builder

        self._deposit_transaction_business_events_topic = "transactions-deposit"
        self._withdrawal_transaction_business_events_topic = "transactions-withdrawal"
        self._payment_transaction_business_events_topic = "transactions-payment"
        self._payments_business_events_topic = "payments"
        self._task_cost_cud_events_topic = "task-cost-stream"

    async def produce_task_cost_created(self, task: entities.Task) -> None:
        task_cost_created_event = self._event_builder.build_task_cost_created_event(task)

        await broker.publish(task_cost_created_event, topic=self._task_cost_cud_events_topic)

    async def produce_deposit_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        enroll_transaction_applied_events = [
            self._event_builder.build_enroll_transaction_applied_event(transaction)
            for transaction in transactions
        ]

        await broker.publish_batch(
            *enroll_transaction_applied_events, topic=self._deposit_transaction_business_events_topic
        )

    async def produce_withdrawal_transactions_applied(
        self, transactions: list[entities.Transaction]
    ) -> None:
        withdraw_transaction_applied_events = [
            self._event_builder.build_withdraw_transaction_applied_event(transaction)
            for transaction in transactions
        ]

        await broker.publish_batch(
            *withdraw_transaction_applied_events, topic=self._withdrawal_transaction_business_events_topic
        )

    async def produce_payment_transactions_applied(self, transactions: list[entities.Transaction]) -> None:
        payment_transaction_applied_events = [
            self._event_builder.build_payment_transaction_applied_event(transaction)
            for transaction in transactions
        ]

        await broker.publish_batch(
            *payment_transaction_applied_events, topic=self._payment_transaction_business_events_topic
        )

    async def produce_payout_done(self, payment: entities.Payment) -> None:
        payout_done_event = self._event_builder.build_payout_done_event(payment)

        await broker.publish(payout_done_event, topic=self._payments_business_events_topic)
