from enum import StrEnum

import sqlalchemy as sa

from domain import entities


metadata_obj = sa.MetaData()


class WorkerRole(StrEnum):
    ACCOUNTANT = "accountant"
    ADMINISTRATOR = "administrator"
    DEVELOPER = "developer"
    MANAGER = "manager"


# TODO: remove excessive fields, add created_at, etc.
workers_table = sa.Table(
    "workers",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("username", sa.String(length=64), unique=True, nullable=False),
    sa.Column("secret", sa.String(length=128), nullable=False),
    sa.Column("email", sa.String(length=64), unique=True, nullable=False),
    sa.Column("role", sa.Enum(WorkerRole, name="role"), nullable=False),
)


def row_to_domain(row: tuple) -> entities.Worker:
    return entities.Worker(
        id_=row[1],
        username=row[2],
        secret=row[3],
        email=row[4],
        role=entities.WorkerRole(str(row[5])),
    )
