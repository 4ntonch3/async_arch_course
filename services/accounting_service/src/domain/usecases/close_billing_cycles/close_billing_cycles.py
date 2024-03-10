from domain import entities, interfaces


class CloseBillingCyclesUsecase:
    def __init__(
        self,
        transactions_repository: interfaces.TransactionsRepository,
        workers_repository: interfaces.WorkersRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._transactions_repository = transactions_repository
        self._workers_repository = workers_repository
        self._message_broker = message_broker

    async def execute(self) -> list[entities.Payment]:
        workers_to_close_billing_cycles = await self._workers_repository.get_all()

        payments = []

        description = "Payment at the end of a billing cycle."
        for worker in workers_to_close_billing_cycles:
            payment = await self._transactions_repository.apply_payment(worker.public_id, description)
            if payment is not None:
                payments.append(payment)

        await self._message_broker.produce_payments_created(payments)
