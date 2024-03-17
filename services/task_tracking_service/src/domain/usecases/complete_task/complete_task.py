from domain import interfaces


class CompleteTaskUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._message_broker = message_broker

    async def execute(self, task_external_id: str) -> None:
        task = await self._tasks_repository.complete(task_external_id)

        await self._message_broker.produce_task_closed(task)

        await self._message_broker.produce_task_completed(task)
