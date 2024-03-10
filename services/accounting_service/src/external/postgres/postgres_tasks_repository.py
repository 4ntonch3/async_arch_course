from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from domain import entities, interfaces

from . import models


class PostgresTasksRepository(interfaces.TasksRepository):
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
        self._session_factory = async_sessionmaker(self._engine)

    async def add(self, public_id: str) -> entities.Task:
        async with self._session_factory() as session:
            new_task_model = await session.scalar(
                sqlalchemy.insert(models.TaskORM).returning(models.TaskORM),
                [
                    {
                        "public_id": public_id,
                        "assign_fee": entities.Task.calculate_assign_fee().to_decimal(),
                        "completion_award": entities.Task.calculate_completion_award().to_decimal(),
                        "created_at": datetime.utcnow(),
                    }
                ],
            )
            new_task = new_task_model.to_domain()

            await session.commit()

        return new_task

    async def get_by_public_id(self, public_id: str) -> entities.Task | None:
        async with self._session_factory() as session:
            select_by_public_id = sqlalchemy.select(models.TaskORM).filter(
                models.TaskORM.public_id == public_id
            )

            select_by_public_id_result = await session.execute(select_by_public_id)

            task_model = select_by_public_id_result.scalars().first()

        if task_model is None:
            return None

        return task_model.to_domain()
