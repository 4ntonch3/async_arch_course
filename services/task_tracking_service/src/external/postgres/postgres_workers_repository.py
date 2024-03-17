import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from domain import entities
from domain.interfaces import WorkersRepository

from . import models


class PostgresWorkersRepository(WorkersRepository):
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

    async def add(self, public_id: str, role: entities.WorkerRole) -> entities.Worker:
        async with self._engine.connect() as conn:
            await conn.execute(models.workers.build_query_to_insert_new(public_id, role))
            await conn.commit()
