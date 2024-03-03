from domain import entities, interfaces


class AddTaskUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        workers_repository: interfaces.WorkersRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._workers_repository = workers_repository
        self._message_broker = message_broker

    async def execute(self, description: str) -> str:
        random_worker = await self._workers_repository.get_random_with_developer_role()

        new_task = entities.Task.new(description, assignee=random_worker)

        await self._tasks_repository.add(new_task)

        await self._message_broker.produce_task_added(new_task)

        return new_task.id_
