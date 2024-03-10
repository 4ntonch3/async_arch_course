import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from domain import entities, interfaces

from . import models


class PostgresPaymentsRepository(interfaces.PaymentsRepository):
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

    async def get_for_processing(self, payment_public_id: str) -> entities.Payment:
        async with self._session_factory() as session:
            payment_model = await self._get_by_public_id(session, payment_public_id)

            payment = payment_model.to_domain()

            if payment.status is entities.PaymentStatus.PROCESSED:
                raise interfaces.payments_repository_error.PaymentAlreadyProcessedError()

            payment.change_status_to_in_progress()

            payment_model.sync_with_domain(payment)

            await session.commit()

        return payment

    async def mark_processed(self, payment_id: str) -> entities.Payment:
        async with self._session_factory() as session:
            payment_model = await self._get_by_id(session, payment_id)

            payment = payment_model.to_domain()

            payment.change_status_to_processed()

            payment_model.sync_with_domain(payment)

            await session.commit()

        return payment

    async def mark_failed(self, payment_id: str) -> entities.Payment:
        async with self._session_factory() as session:
            payment_model = await self._get_by_id(session, payment_id)

            payment = payment_model.to_domain()

            payment.change_status_to_failed()

            payment_model.sync_with_domain(payment)

            await session.commit()

        return payment

    async def _get_by_public_id(self, session: AsyncSession, payment_public_id: str) -> models.PaymentORM:
        select_by_public_id = sqlalchemy.select(models.PaymentORM).filter(
            models.PaymentORM.public_id == payment_public_id
        )

        select_by_public_id_result = await session.execute(select_by_public_id)

        return select_by_public_id_result.scalars().first()

    async def _get_by_id(self, session: AsyncSession, payment_id: str) -> models.PaymentORM:
        select_by_id = sqlalchemy.select(models.PaymentORM).filter(models.PaymentORM.id == int(payment_id))

        select_by_id_result = await session.execute(select_by_id)

        return select_by_id_result.scalars().first()
