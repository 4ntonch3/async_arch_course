import uuid

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from domain import entities
from domain.interfaces import TasksRepository

from . import models


class PostgresTasksRepository(TasksRepository):
    def __init__(self, host: str, port: int, user: str, password: str, database_title: str) -> None:
        url = sqlalchemy.URL(
            drivername="postgresql+asyncpg",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database_title,
            query={},
        )
        self._engine = create_async_engine(url)

    async def add(self, jira_id: str | None, description: str) -> entities.Task:
        async with self._engine.connect() as conn:
            random_developer_model = await conn.execute(
                models.workers.build_query_to_select_random_with_role(entities.WorkerRole.DEVELOPER)
            )
            random_developer = models.workers.build_domain_from_model(random_developer_model.first())

            insert_task = models.tasks.build_query_to_insert_new(
                public_id=str(uuid.uuid4()),
                external_id=str(uuid.uuid4()),
                assignee_id=int(random_developer.id),
                description=description,
                status=entities.TaskStatus.OPEN,
                jira_id=jira_id,
            )
            insert_task_result = await conn.execute(insert_task)

            task = models.tasks.build_domain_from_model(insert_task_result.first(), random_developer)

            await conn.commit()

        return task

    async def complete(self, external_id: str) -> entities.Task:
        # TODO: add check if not exist?
        async with self._engine.connect() as conn:
            await conn.execute(
                models.tasks.build_query_to_update_status_by_external_id(
                    external_id, status=entities.TaskStatus.COMPLETED
                )
            )

            select_task_by_external_id_result = await conn.execute(
                models.tasks.build_query_to_select_by_external_id(external_id)
            )
            task = models.tasks.build_domain_from_extended_model(select_task_by_external_id_result.first())

            await conn.commit()

        return task

    async def get_all_for_worker(self, worker_public_id: str) -> list[entities.Task]:
        async with self._engine.connect() as conn:
            select_all_tasks_for_worker = models.tasks.build_query_to_select_all_by_worker_public_id(
                worker_public_id
            )

            all_tasks_for_worker_result = await conn.execute(select_all_tasks_for_worker)

            return [
                models.tasks.build_domain_from_extended_model(task_with_worker_model)
                for task_with_worker_model in all_tasks_for_worker_result.all()
            ]

    async def reassign_all_open(self) -> list[entities.Task]:
        async with self._engine.connect() as conn:
            select_ids_of_open_tasks = models.tasks.build_query_to_select_ids_of_tasks_with_status(
                entities.TaskStatus.OPEN
            )

            select_ids_of_open_tasks_result = await conn.execute(select_ids_of_open_tasks)

            changed_tasks_ids = []

            # TODO: add streaming
            for open_task_id in select_ids_of_open_tasks_result.all():
                open_task_id = int(open_task_id[0])
                random_developer = await self._get_random_developer(conn)

                await conn.execute(
                    models.tasks.build_query_to_update_assignee_by_id(open_task_id, int(random_developer.id))
                )

                changed_tasks_ids.append(open_task_id)

            select_all_changed_tasks = models.tasks.build_query_to_select_tasks_by_ids(changed_tasks_ids)

            select_all_changed_tasks_result = await conn.execute(select_all_changed_tasks)

            changed_tasks = [
                models.tasks.build_domain_from_extended_model(task_with_worker_model)
                for task_with_worker_model in select_all_changed_tasks_result.all()
            ]

            await conn.commit()

        return changed_tasks

    async def _get_random_developer(self, connection: AsyncConnection) -> entities.Worker:
        select_random_developer_result = await connection.execute(
            models.workers.build_query_to_select_random_with_role(entities.WorkerRole.DEVELOPER)
        )

        return models.workers.build_domain_from_model(select_random_developer_result.first())
