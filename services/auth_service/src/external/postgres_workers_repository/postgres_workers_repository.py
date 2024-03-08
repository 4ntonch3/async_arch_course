import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from domain import entities
from domain.interfaces import WorkersRepository

from .models import row_to_domain, workers_table


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

    async def add(self, worker: entities.Worker) -> None:
        insert_worker = workers_table.insert().values(
            public_id=worker.public_id,
            username=worker.username,
            secret=worker.secret,
            email=worker.email,
            role=worker.role,
        )

        async with self._engine.connect() as conn:
            await conn.execute(insert_worker)
            await conn.commit()

    async def get(self, username: str, secret: str) -> entities.Worker:
        select_worker = workers_table.select().where(
            workers_table.c.username == username,
            workers_table.c.secret == secret,
        )

        async with self._engine.connect() as conn:
            result = await conn.execute(select_worker)
            worker_row = result.first()

        return row_to_domain(worker_row)
