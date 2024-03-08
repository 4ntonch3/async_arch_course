from datetime import datetime
from typing import AsyncIterator

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from domain import entities
from domain.interfaces import TasksRepository

from ..workers_repository.models import workers_table  # TODO
from .models import TaskStatus, row_to_dto, tasks_table


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

    async def add(self, task: entities.Task) -> None:
        now = datetime.utcnow()

        insert_task = tasks_table.insert().values(
            public_id=task.public_id,
            worker_public_id=task.assignee.id_,
            created_at=now,
            updated_at=now,
            description=task.description,
            status=TaskStatus(str(task.status)),
        )

        async with self._engine.connect() as conn:
            await conn.execute(insert_task)
            await conn.commit()

    async def get(self, task_public_id: str) -> entities.Task:
        select_task = (
            tasks_table.join(workers_table, tasks_table.c.worker_public_id == workers_table.c.public_id)
            .select()
            .where(tasks_table.c.public_id == task_public_id)
        )

        async with self._engine.connect() as conn:
            result = await conn.execute(select_task)

            task_row = result.first()

        return row_to_dto(task_row)

    async def get_all_for_worker(self, worker_public_id: str) -> list[entities.Task]:
        select_tasks_for_worker = (
            tasks_table.join(workers_table, tasks_table.c.worker_public_id == workers_table.c.public_id)
            .select()
            .where(workers_table.c.public_id == worker_public_id)
        )

        async with self._engine.connect() as conn:
            result = await conn.execute(select_tasks_for_worker)

            return [row_to_dto(task_row) for task_row in result.all()]

    async def update(self, task: entities.Task) -> None:
        # TODO: add check if not exist?
        update_task = (
            tasks_table.update()
            .where(tasks_table.c.public_id == task.public_id)
            .values(
                updated_at=datetime.utcnow(),
                description=task.description,
                status=task.status,
            )
        )

        async with self._engine.connect() as conn:
            await conn.execute(update_task)
            await conn.commit()

    async def stream_opened(self) -> AsyncIterator[entities.Task]:
        select_all = (
            tasks_table.join(workers_table, tasks_table.c.worker_public_id == workers_table.c.public_id)
            .select()
            .where(tasks_table.c.status == entities.TaskStatus.OPENED)
        )

        # TODO: add streaming
        async with self._engine.connect() as conn:
            result = await conn.execute(select_all)

            tasks_rows = result.all()

        for task_row in tasks_rows:
            yield row_to_dto(task_row)
