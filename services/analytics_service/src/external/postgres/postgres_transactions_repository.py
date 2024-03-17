from datetime import date, datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from domain import entities
from domain.interfaces import TransactionsRepository

from . import models


class PostgresTransactionsRepository(TransactionsRepository):
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
        worker_public_id: str,
        type: entities.TransactionType,
        value: entities.Money,
        created_at: datetime,
    ) -> entities.Transaction:
        async with self._engine.connect() as conn:
            insert_transaction = models.transaction.table.insert().values(
                public_id=public_id,
                type=str(type),
                value=value,
                created_at=created_at,
            )
            await conn.execute(insert_transaction)

            select_worker_by_public_id = models.worker.table.select().where(
                models.worker.table.c.public_id == worker_public_id
            )
            select_worker_by_public_id_result = await conn.execute(select_worker_by_public_id)
            worker = models.worker.build_domain_from_model(select_worker_by_public_id_result.first())

            match type:
                case entities.TransactionType.WITHDRAWAL:
                    worker.balance += value
                case entities.TransactionType.DEPOSIT:
                    worker.balance -= value
                case entities.TransactionType.PAYMENT:
                    worker.balance -= value

            update_worker_balance = (
                models.worker.table.update()
                .where(models.worker.table.c.id == int(worker.id))
                .values(balance=worker.balance)
            )
            await conn.execute(update_worker_balance)

            await conn.commit()

    async def get_todays_managers_profit(self) -> entities.Money:
        async with self._engine.connect() as conn:
            select_credit_sum = sqlalchemy.select(
                sqlalchemy.func.sum(models.transaction.table.c.value).filter(
                    sqlalchemy.cast(models.transaction.table.c.created_at, sqlalchemy.Date) == date.today(),
                    models.transaction.table.c.type == entities.TransactionType.WITHDRAWAL,
                )
            )

            select_debit_sum = sqlalchemy.select(
                sqlalchemy.func.sum(models.transaction.table.c.value).filter(
                    sqlalchemy.cast(models.transaction.table.c.created_at, sqlalchemy.Date) == date.today(),
                    models.transaction.table.c.type == entities.TransactionType.DEPOSIT,
                )
            )

            credit_sum_result = await conn.execute(select_credit_sum)
            debit_sum_result = await conn.execute(select_debit_sum)

            credit_sum = credit_sum_result.first()[0]
            debit_sum = debit_sum_result.first()[0]

        return entities.Money(debit_sum) - entities.Money(credit_sum)
