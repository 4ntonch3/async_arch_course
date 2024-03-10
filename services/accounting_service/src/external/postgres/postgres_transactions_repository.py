import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import joinedload

from domain import entities, interfaces

from . import models


class PostgresTransactionsRepository(interfaces.TransactionsRepository):
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

    async def apply_enroll(
        self, worker_public_id: str, value: entities.Money, description: str
    ) -> entities.Transaction:
        async with self._session_factory() as session:
            billing_cycle_model = await self._get_open_billing_cycle_for_worker(session, worker_public_id)
            billing_cycle = billing_cycle_model.to_domain()

            worker_model = billing_cycle_model.worker
            worker = worker_model.to_domain()

            new_transaction_model = await session.scalar(
                sqlalchemy.insert(models.TransactionORM).returning(models.TransactionORM),
                [
                    {
                        "public_id": str(uuid.uuid4()),
                        "worker_id": int(worker.id),
                        "billing_cycle_id": int(billing_cycle.id),
                        "type": str(entities.TransactionType.ENROLL),
                        "credit": entities.Money(0).to_decimal(),
                        "debit": value.to_decimal(),
                        "description": description,
                        "created_at": datetime.utcnow(),
                    }
                ],
            )
            transaction = new_transaction_model.to_domain()

            worker.balance += transaction.debit
            worker_model.sync_with_domain(worker)

            await session.commit()

        return transaction

    async def apply_withdraw(
        self, worker_public_id: str, value: entities.Money, description: str
    ) -> entities.Transaction:
        async with self._session_factory() as session:
            billing_cycle_model = await self._get_open_billing_cycle_for_worker(session, worker_public_id)
            billing_cycle = billing_cycle_model.to_domain()

            worker_model = billing_cycle_model.worker
            worker = worker_model.to_domain()

            new_transaction_model = await session.scalar(
                sqlalchemy.insert(models.TransactionORM).returning(models.TransactionORM),
                [
                    {
                        "public_id": str(uuid.uuid4()),
                        "worker_id": int(worker.id),
                        "billing_cycle_id": int(billing_cycle.id),
                        "type": str(entities.TransactionType.WITHDRAW),
                        "credit": value.to_decimal(),
                        "debit": entities.Money(0).to_decimal(),
                        "description": description,
                        "created_at": datetime.utcnow(),
                    }
                ],
            )
            transaction = new_transaction_model.to_domain()

            worker.balance -= transaction.credit
            worker_model.sync_with_domain(worker)

            await session.commit()

        return transaction

    async def apply_payment(self, worker_public_id: str, description: str) -> entities.Payment | None:
        async with self._session_factory() as session:
            billing_cycle_model = await self._get_open_billing_cycle_for_worker(session, worker_public_id)
            billing_cycle = billing_cycle_model.to_domain()

            worker_model = billing_cycle_model.worker
            worker = worker_model.to_domain()

            payment = None
            if worker.balance > 0:
                new_transaction_model = await session.scalar(
                    sqlalchemy.insert(models.TransactionORM).returning(models.TransactionORM),
                    [
                        {
                            "public_id": str(uuid.uuid4()),
                            "worker_id": int(worker.id),
                            "billing_cycle_id": int(billing_cycle.id),
                            "type": str(entities.TransactionType.PAYMENT),
                            "credit": entities.Money(0).to_decimal(),
                            "debit": worker.balance.to_decimal(),
                            "description": description,
                            "created_at": datetime.utcnow(),
                        }
                    ],
                )
                transaction = new_transaction_model.to_domain()

                worker.balance = 0
                worker_model.sync_with_domain(worker)

                new_payment_model = await session.scalar(
                    sqlalchemy.insert(models.PaymentORM).returning(models.PaymentORM),
                    [
                        {
                            "public_id": str(uuid.uuid4()),
                            "status": str(entities.PaymentStatus.CREATED),
                            "transaction_id": int(transaction.id),
                            "billing_cycle_id": int(billing_cycle.id),
                            "created_at": datetime.utcnow(),
                        }
                    ],
                )
                payment = new_payment_model.to_domain()

            billing_cycle.close()
            billing_cycle_model.sync_with_domain(billing_cycle)

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

        return payment

    async def get_all_for_worker(self, worker_public_id: str) -> list[entities.Transaction]:
        async with self._session_factory() as session:
            select_transactions_for_worker = (
                sqlalchemy.select(models.TransactionORM)
                .options(joinedload(models.TransactionORM.worker))
                .options(joinedload(models.TransactionORM.billing_cycle))
                .filter(models.WorkerORM.public_id == worker_public_id)
            )

            select_transactions_for_worker_result = await session.execute(select_transactions_for_worker)

            transactions_models = select_transactions_for_worker_result.scalars().all()

            return [transaction_model.to_domain() for transaction_model in transactions_models]

    async def get_daily_enroll_and_withdraw_difference(self) -> entities.Money:
        # TODO: just stub for now
        return entities.Money(0)

    async def _get_open_billing_cycle_for_worker(
        self, session: AsyncSession, worker_public_id: str
    ) -> models.BillingCycleORM:
        select_open_billing_cycle_for_worker = (
            sqlalchemy.select(models.BillingCycleORM)
            .options(joinedload(models.BillingCycleORM.worker))
            .join(models.BillingCycleORM.worker)
            .filter(
                sqlalchemy.and_(
                    models.WorkerORM.public_id == worker_public_id,
                    models.BillingCycleORM.status == str(models.BillingCycleORM.Status.OPEN),
                )
            )
        )

        select_open_billing_cycle_for_worker_result = await session.execute(
            select_open_billing_cycle_for_worker
        )

        return select_open_billing_cycle_for_worker_result.scalars().first()
