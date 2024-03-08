from domain import entities, interfaces


class ReassignTasksUsecase:
    def __init__(
        self,
        tasks_repository: interfaces.TasksRepository,
        workers_repository: interfaces.WorkersRepository,
        message_broker: interfaces.MessageBroker,
    ) -> None:
        self._tasks_repository = tasks_repository
        self._workers_repository = workers_repository
        self._message_broker = message_broker

        # just to ensure we don't have parallel reassign on 1 instance
        self._is_reassign_active = False

    async def execute(self) -> None:
        if self._is_reassign_active:
            msg_exc = "Reassign is already active."
            raise RuntimeError(msg_exc)  # TODO

        self._is_reassign_active = True

        reassigned_tasks = []

        async for task in self._tasks_repository.stream_opened():
            reassigned_task = await self._reassign_task(task)
            reassigned_tasks.append(reassigned_task)

        await self._message_broker.produce_tasks_assigned(reassigned_tasks)

        self._is_reassign_active = False

    async def _reassign_task(self, task: entities.Task) -> entities.Task:
        random_worker = await self._workers_repository.get_random_with_developer_role()

        task.reassign(new_assignee=random_worker)

        await self._tasks_repository.update(task)

        return task
