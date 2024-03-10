from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

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

    async def add(
        self,
        public_id: str,
        status: entities.TaskStatus,
        cost: entities.Money | None,
        created_at: datetime,
        closed_at: datetime | None,
    ) -> entities.Task:
        insert_task = (
            models.task.table.insert()
            .values(
                public_id=public_id,
                status=str(status),
                cost=cost,
                created_at=created_at,
                closed_at=closed_at,
            )
            .returning(models.task.table)
        )

        async with self._engine.connect() as conn:
            insert_task_result = await conn.execute(insert_task)
            new_task_model = insert_task_result.first()

            new_task = models.task.row_to_domain(new_task_model)

            await conn.commit()

        return new_task

    async def close(self, public_id: str) -> None:
        update_to_close_task = (
            models.task.table.update()
            .where(models.task.table.c.public_id == public_id)
            .values(status=str(models.task.TaskStatus.CLOSED), closed_at=datetime.utcnow())
        )

        async with self._engine.connect() as conn:
            await conn.execute(update_to_close_task)
            await conn.commit()

    async def get_most_expensive(self, start_date: datetime, end_date: datetime) -> entities.Task:
        select_most_expensive_closed_task = (
            models.task.table.select()
            .where(
                sqlalchemy.and_(
                    models.task.table.c.status == str(models.task.TaskStatus.CLOSED),
                    models.task.table.c.closed_at.between(start_date, end_date),
                )
            )
            .order_by(models.task.table.c.cost)
            .limit(1)
        )

        async with self._engine.connect() as conn:
            result = await conn.execute(select_most_expensive_closed_task)
            task_row = result.first()

            return models.task.row_to_domain(task_row)

    async def set_cost(self, public_id: str, cost: entities.Money) -> None:
        update_to_set_cost = (
            models.task.table.update().where(models.task.table.c.public_id == public_id).values(cost=cost)
        )

        async with self._engine.connect() as conn:
            await conn.execute(update_to_set_cost)
            await conn.commit()
