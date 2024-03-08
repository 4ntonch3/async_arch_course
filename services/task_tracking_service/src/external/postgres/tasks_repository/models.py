from enum import StrEnum

import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


class TaskStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"


tasks_table = sa.Table(
    "tasks",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("worker_public_id", sa.String(length=64), sa.ForeignKey("workers.public_id"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("description", sa.String(length=1024), nullable=False),
    sa.Column("status", sa.Enum(TaskStatus, name="status"), nullable=False),
)


def row_to_dto(row: tuple) -> entities.Task:
    return entities.Task(
        public_id=row[1],
        assignee=entities.Worker(row[2], entities.WorkerRole(str(row[9]))),
        description=row[5],
        status=entities.TaskStatus(str(row[6])),
    )
