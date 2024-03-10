from enum import StrEnum

import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


class TaskStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"


table = sa.Table(
    "tasks",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("status", sa.Enum(TaskStatus, name="status"), nullable=False),
    sa.Column("cost", sa.Numeric(precision=8, scale=3), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
)


def row_to_domain(row: tuple) -> entities.Task:
    return entities.Task(
        id=str(row[0]),
        public_id=row[1],
        status=entities.TaskStatus(str(row[2])),
        cost=entities.Money(row[3]) if row[3] is not None else None,
        created_at=row[4],
        closed_at=row[5],
    )
