from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from domain import entities, interfaces

from . import models


class PostgresWorkersRepository(interfaces.WorkersRepository):
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

    async def add(self, public_id: str, email: str, role: entities.WorkerRole) -> entities.Worker:
        async with self._session_factory() as session:
            new_worker_model = await session.scalar(
                sqlalchemy.insert(models.WorkerORM).returning(models.WorkerORM),
                [
                    {
                        "public_id": public_id,
                        "balance": entities.Money(0).to_decimal(),
                        "email": email,
                        "role": str(role),
                        "created_at": datetime.utcnow(),
                    }
                ],
            )
            worker = new_worker_model.to_domain()

            await session.scalar(
                sqlalchemy.insert(models.BillingCycleORM).returning(models.BillingCycleORM),
                [
                    {
                        "worker_id": int(worker.id),
                        "payment_id": None,
                        "status": str(entities.BillingCycleStatus.OPEN),
                        "started_at": datetime.utcnow(),
                        "ended_at": None,
                    }
                ],
            )

            await session.commit()

        return worker

    async def get_all(self) -> list[entities.Worker]:
        async with self._session_factory() as session:
            select_workers = sqlalchemy.select(models.WorkerORM)

            select_worker_result = await session.execute(select_workers)

            return [worker_model.to_domain() for worker_model in select_worker_result.scalars().all()]

    async def get_by_public_id(self, public_id: str) -> entities.Worker:
        async with self._session_factory() as session:
            select_worker_by_public_id = sqlalchemy.select(models.WorkerORM).where(
                models.WorkerORM.public_id == public_id
            )

            select_worker_by_public_id_result = await session.execute(select_worker_by_public_id)
            worker_model = select_worker_by_public_id_result.scalars().first()

            return worker_model.to_domain()
