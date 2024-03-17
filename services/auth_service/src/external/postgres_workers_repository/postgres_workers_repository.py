import uuid

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

    async def add(self, username: str, secret_hash: str, role: entities.WorkerRole) -> entities.Worker:
        async with self._engine.connect() as conn:
            insert_new_result = await conn.execute(
                models.workers.build_query_to_insert_new(
                    public_id=str(uuid.uuid4()), username=username, secret_hash=secret_hash, role=role
                )
            )

            worker_model = insert_new_result.first()
            worker = models.workers.build_domain_from_model(worker_model)

            await conn.commit()

        return worker

    async def get_by_username(self, username: str) -> entities.Worker:
        async with self._engine.connect() as conn:
            select_by_username_result = await conn.execute(
                models.workers.build_query_to_select_by_username(username)
            )
            worker_model = select_by_username_result.first()

            return models.workers.build_domain_from_model(worker_model)
