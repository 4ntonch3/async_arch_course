from datetime import UTC, datetime

import sqlalchemy as sa

from domain import entities

from .common import metadata_obj
from .workers import table as workers_table


table = sa.Table(
    "tasks",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("external_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("assignee_id", sa.Integer, sa.ForeignKey("workers.id"), nullable=False),
    sa.Column("jira_id", sa.String(length=64), nullable=True),
    sa.Column("description", sa.String(length=1024), nullable=False),
    sa.Column("status", sa.Enum(entities.TaskStatus, name="status"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)


def build_domain_from_model(model: tuple, assignee: entities.Worker) -> entities.Task:
    return entities.Task(
        id=model[0],
        public_id=model[1],
        external_id=model[2],
        jira_id=model[4],
        assignee=assignee,
        description=model[5],
        status=model[6],
    )


def build_domain_from_extended_model(task_with_worker_model: tuple) -> entities.Task:
    return entities.Task(
        id=str(task_with_worker_model[0]),
        public_id=task_with_worker_model[1],
        external_id=task_with_worker_model[2],
        jira_id=task_with_worker_model[4],
        assignee=entities.Worker(
            id=str(task_with_worker_model[9]),
            public_id=task_with_worker_model[10],
            role=entities.WorkerRole(task_with_worker_model[11].lower()),
        ),
        description=task_with_worker_model[5],
        status=task_with_worker_model[6],
    )


def build_query_to_select_by_external_id(external_id: str) -> sa.Select:
    return (
        table.join(workers_table, table.c.assignee_id == workers_table.c.id)
        .select()
        .where(table.c.external_id == external_id)
    )


def build_query_to_select_ids_of_tasks_with_status(status: entities.TaskStatus) -> sa.Select:
    return table.select().where(table.c.status == status).with_only_columns(table.c.id)


def build_query_to_select_all_by_worker_public_id(worker_public_id: str) -> sa.Select:
    return (
        table.join(workers_table, table.c.assignee_id == workers_table.c.id)
        .select()
        .where(workers_table.c.public_id == worker_public_id)
    )


def build_query_to_select_tasks_by_ids(ids: list[int]) -> sa.Select:
    return (
        table.join(workers_table, table.c.assignee_id == workers_table.c.id)
        .select()
        .where(table.c.id.in_(ids))
    )


def build_query_to_insert_new(
    public_id: str,
    external_id: str,
    assignee_id: int,
    description: str,
    status: entities.TaskStatus,
    jira_id: str | None,
) -> sa.Insert:
    now = datetime.now(UTC)

    return (
        table.insert()
        .values(
            public_id=public_id,
            external_id=external_id,
            assignee_id=assignee_id,
            jira_id=jira_id,
            description=description,
            status=status,
            created_at=now,
            updated_at=now,
        )
        .returning(sa.literal_column("*"))
    )


def build_query_to_update_status_by_external_id(external_id: str, status: entities.TaskStatus) -> sa.Update:
    return (
        table.update().values(updated_at=datetime.now(UTC), status=status).filter_by(external_id=external_id)
    )


def build_query_to_update_assignee_by_id(id_: int, assignee_id: int) -> sa.Update:
    return table.update().values(updated_at=datetime.now(UTC), assignee_id=assignee_id).filter_by(id=id_)
