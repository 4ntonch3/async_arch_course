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
        insert_worker = (
            models.worker.table.insert()
            .values(
                public_id=public_id,
                role=str(role),
                balance=entities.Money(0),
            )
            .returning(models.worker.table)
        )
        async with self._engine.connect() as conn:
            insert_worker_result = await conn.execute(insert_worker)
            new_worker_model = insert_worker_result.first()

            new_worker = models.worker.build_domain_from_model(new_worker_model)

            await conn.commit()

        return new_worker

    async def get_workers_with_negative_balance(self) -> list[entities.Worker]:
        select_workers_with_negative_balance = models.worker.table.select().where(
            models.worker.table.c.balance < 0
        )

        async with self._engine.connect() as conn:
            select_workers_with_negative_balance_result = await conn.execute(
                select_workers_with_negative_balance
            )
            workers_models = select_workers_with_negative_balance_result.all()

            return [models.worker.build_domain_from_model(worker_model) for worker_model in workers_models]
