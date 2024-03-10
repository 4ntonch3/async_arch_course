from enum import StrEnum

import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


class WorkerRole(StrEnum):
    ADMINISTATOR = "administrator"
    ACCOUNTANT = "accountant"
    DEVELOPER = "developer"
    MANAGER = "manager"


table = sa.Table(
    "workers",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("role", sa.Enum(WorkerRole, name="role"), nullable=False),
    sa.Column("balance", sa.Numeric(precision=8, scale=3), nullable=False),
)


def row_to_domain(row: tuple) -> entities.Worker:
    return entities.Worker(
        id=str(row[0]),
        public_id=row[1],
        role=entities.WorkerRole(str(row[2])),
        balance=entities.Money(row[3]),
    )
