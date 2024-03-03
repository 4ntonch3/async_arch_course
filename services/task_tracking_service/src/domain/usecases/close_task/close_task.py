from domain import interfaces


class CloseTaskUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._message_broker = message_broker

    async def execute(self, task_id: str) -> None:
        # TODO: add transaction to get & update
        task = await self._tasks_repository.get(task_id)

        task.close()

        await self._tasks_repository.update(task)

        await self._message_broker.produce_task_closed(task)
