from domain import entities, interfaces


class WorkerPayoutUsecase:
    def __init__(
        self,
        payments_repository: interfaces.PaymentsRepository,
        message_broker: interfaces.MessageBroker,
        bank_client: interfaces.BankClient,
        email_client: interfaces.EmailClient,
    ) -> None:
        self._payments_repository = payments_repository
        self._message_broker = message_broker
        self._bank_client = bank_client
        self._email_client = email_client

    async def execute(self, payment_public_id: str) -> None:
        try:
            payment = await self._payments_repository.get_for_processing(payment_public_id)
        except interfaces.payments_repository_error.PaymentAlreadyProcessedError:
            return

        try:
            await self._bank_client.transfer(payment.transaction.worker.public_id, payment.transaction.debit)
        except Exception:
            self._payments_repository.mark_failed(payment.id)
            return

        payment = await self._payments_repository.mark_processed(payment.id)
        await self._message_broker.produce_payment_processed(payment)

        await self._email_client.send(
            payment.transaction.worker.email, self._construct_notification_message(payment)
        )

    def _construct_notification_message(self, payment: entities.Payment) -> str:
        return f"Date: {payment.transaction.created_at}.\nPayed Out: {payment.transaction.debit}"
