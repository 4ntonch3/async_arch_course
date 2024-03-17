from datetime import UTC, datetime

import sqlalchemy as sa

from domain import entities


metadata_obj = sa.MetaData()


table = sa.Table(
    "workers",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("username", sa.String(length=64), unique=True, nullable=False),
    sa.Column("secret_hash", sa.String(length=128), nullable=False),  # TODO: add salt
    sa.Column("role", sa.Enum(entities.WorkerRole, name="role"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)


def build_domain_from_model(model: tuple) -> entities.Worker:
    return entities.Worker(
        id=str(model[0]),
        public_id=model[1],
        username=model[2],
        hashed_secret=model[3],
        role=entities.WorkerRole(model[4].lower()),
    )


def build_query_to_insert_new(
    public_id: str, username: str, secret_hash: str, role: entities.WorkerRole
) -> sa.Insert:
    now = datetime.now(UTC)

    return (
        table.insert()
        .values(
            public_id=public_id,
            username=username,
            secret_hash=secret_hash,
            role=str(role),
            created_at=now,
            updated_at=now,
        )
        .returning(sa.literal_column("*"))
    )


def build_query_to_select_by_username(username: str) -> sa.Select:
    return table.select().where(table.c.username == username)
