from datetime import UTC, datetime

import sqlalchemy as sa

from domain import entities

from .common import metadata_obj


table = sa.Table(
    "workers",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("role", sa.Enum(entities.WorkerRole, name="role"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)


def build_domain_from_model(model: tuple) -> entities.Worker:
    return entities.Worker(id=str(model[0]), public_id=model[1], role=model[2])


def build_query_to_insert_new(
    public_id: str,
    role: entities.WorkerRole,
) -> sa.Insert:
    now = datetime.now(UTC)

    return table.insert().values(
        public_id=public_id,
        role=role,
        created_at=now,
        updated_at=now,
    )


def build_query_to_select_random_with_role(role: entities.WorkerRole) -> sa.Select:
    return table.select().order_by(sa.func.random()).limit(limit=1).where(table.c.role == role)
