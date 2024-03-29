import asyncio

from domain import interfaces


class ApplyWithdrawalTransactionUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        transactions_repository: interfaces.TransactionsRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._transactions_repository = transactions_repository
        self._message_broker = message_broker

    async def execute(self, task_public_id: str, worker_public_id: str, description: str) -> None:
        task = None
        interval_between_info_fetch = 0.5
        # TODO: remove infinite loop
        while task is None:
            task = await self._tasks_repository.get_by_public_id(task_public_id)
            await asyncio.sleep(interval_between_info_fetch)

        transaction = await self._transactions_repository.apply_withdrawal(
            worker_public_id, task.cost.completion_award, description
        )

        await self._message_broker.produce_withdrawal_transactions_applied([transaction])
