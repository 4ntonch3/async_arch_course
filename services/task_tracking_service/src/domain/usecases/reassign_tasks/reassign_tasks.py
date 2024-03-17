from domain import interfaces


class ReassignTasksUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._message_broker = message_broker

    async def execute(self) -> None:
        reassigned_tasks = await self._tasks_repository.reassign_all_open()

        await self._message_broker.produce_tasks_assigned(reassigned_tasks)
