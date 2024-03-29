import asyncio
import re
import uuid
from datetime import UTC, datetime

import sqlalchemy as sa
from faststream.kafka import KafkaBroker
from schema_registry import EventType, SchemaRegistry
from sqlalchemy.ext.asyncio import create_async_engine

import environment as env
from domain import entities


broker = KafkaBroker(f"{env.BROKER_HOST}:{env.BROKER_PORT}")
schema_registry = SchemaRegistry()


metadata_obj = sa.MetaData()
engine = create_async_engine("postgresql+asyncpg://user:example@localhost:5432/task_tracker")

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


def build_domain_from_model(model: tuple) -> entities.Task:
    return entities.Task(
        id=model[0],
        public_id=model[1],
        external_id=model[2],
        jira_id=model[4],
        assignee=None,
        description=model[5],
        status=model[6],
    )


async def migrate_data() -> None:
    updated_tasks = []

    tasks = await _get_all_tasks()

    for task in tasks:
        description_mask = r"^(?P<jira_id>\[.*?\])?(?P<description>.*?)$"
        regex_search = re.search(description_mask, task.description)

        jira_id = regex_search.group("jira_id")
        description = regex_search.group("description")

        if not jira_id:
            continue

        task = await _update_task(task.id, jira_id, description)
        updated_tasks.append(task)

    await _produce_tasks_updated_events(updated_tasks)


async def _get_all_tasks() -> list[entities.Task]:
    async with engine.connect() as conn:
        select_all_tasks_results = await conn.execute(table.select())

        return [build_domain_from_model(task_model) for task_model in select_all_tasks_results.all()]


async def _update_task(task: entities.Task, jira_id: str, description: str) -> entities.Task:
    async with engine.connect() as conn:
        update_task = (
            table.update()
            .where(table.c.id == task.id)
            .values(
                jira_id=jira_id,
                description=description,
            )
        ).returning(sa.literal_column("*"))

        update_task_result = await conn.execute(update_task)

        return build_domain_from_model(update_task_result.first())


async def _produce_tasks_updated_events(tasks: list[entities.Task]) -> None:
    await broker.publish_batch(
        *[_build_task_updated_event(task) for task in tasks],
        topic="task-stream",
    )


def _build_task_updated_event(task: entities.Task) -> dict:
    version = "1"
    event = {
        "event_id": str(uuid.uuid4()),
        "event_version": version,
        "event_name": "TaskUpdated",
        "event_time": datetime.now(UTC).ctime(),
        "producer": "task-tracker",
        "payload": {
            "public_id": task.public_id,
            "assigned_worker_public_id": task.assignee.public_id,
        },
    }

    schema_registry.validate_event(event, EventType.TASK_UPDATED, version)

    return event


if __name__ == "__main__":
    asyncio.run(migrate_data())
