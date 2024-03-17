import re

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

    async def execute(self, description: str) -> entities.Task:
        description_mask = r"^(?P<jira_id>\[.*?\])?(?P<description>.*?)$"
        regex_search = re.search(description_mask, description)

        jira_id = regex_search.group("jira_id")
        description = regex_search.group("description")

        new_task = await self._tasks_repository.add(jira_id, description)

        await self._message_broker.produce_task_created(new_task)
        await self._message_broker.produce_task_added(new_task)

        return new_task
