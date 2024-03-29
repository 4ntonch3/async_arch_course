from datetime import UTC, datetime

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
        created_at: datetime,
        closed_at: datetime | None,
    ) -> entities.Task:
        async with self._engine.connect() as conn:
            insert_task = (
                models.task.table.insert()
                .values(
                    public_id=public_id,
                    status=str(status),
                    task_cost_id=None,
                    created_at=created_at,
                    closed_at=closed_at,
                )
                .returning(sqlalchemy.literal_column("*"))
            )
            insert_task_result = await conn.execute(insert_task)
            new_task_model = insert_task_result.first()

            new_task = models.task.build_domain_from_model(new_task_model, cost=None)

            await conn.commit()

        return new_task

    async def close(self, public_id: str) -> None:
        update_to_close_task = (
            models.task.table.update()
            .where(models.task.table.c.public_id == public_id)
            .values(status=entities.TaskStatus.COMPLETED, closed_at=datetime.now(UTC))
        )

        async with self._engine.connect() as conn:
            await conn.execute(update_to_close_task)
            await conn.commit()

    async def get_most_expensive(self, start_date: datetime, end_date: datetime) -> entities.Task:
        # TODO
        select_most_expensive_closed_task = (
            models.task.table.join(
                models.task_cost.table, models.task.table.c.task_cost_id == models.task_cost.table.c.id
            )
            .select()
            .where(
                models.task.table.c.status == str(entities.TaskStatus.COMPLETED),
                # sqlalchemy.and_(
                #     models.task.table.c.status == str(entities.TaskStatus.COMPLETED),
                #     models.task.table.c.closed_at.between(start_date, end_date),
                # )
            )
            .order_by(models.task_cost.table.c.completion_award)
            .limit(1)
        )

        async with self._engine.connect() as conn:
            result = await conn.execute(select_most_expensive_closed_task)
            task_row = result.first()

            return models.task.build_domain_from_extended_model(task_row)

    async def set_cost(
        self,
        task_public_id: str,
        cost_public_id: str,
        assign_fee: entities.Money,
        completion_award: entities.Money,
    ) -> None:
        async with self._engine.connect() as conn:
            insert_cost = (
                models.task_cost.table.insert()
                .values(public_id=cost_public_id, assign_fee=assign_fee, completion_award=completion_award)
                .returning(sqlalchemy.literal_column("*"))
            )
            insert_cost_result = await conn.execute(insert_cost)

            update_to_set_cost = (
                models.task.table.update()
                .where(models.task.table.c.public_id == task_public_id)
                .values(task_cost_id=int(insert_cost_result.first()[0]))
            )
            await conn.execute(update_to_set_cost)

            await conn.commit()
