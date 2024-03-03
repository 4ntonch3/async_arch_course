from enum import StrEnum

import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


class WorkerRole(StrEnum):
    ADMINISTATOR = "administrator"
    ACCOUNTANT = "accountant"
    DEVELOPER = "developer"
    MANAGER = "manager"


workers_table = sa.Table(
    "workers",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("role", sa.Enum(WorkerRole, name="role"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)


def row_to_domain(row: tuple) -> entities.Worker:
    return entities.Worker(id_=row[1], role=entities.WorkerRole(str(row[2])))
