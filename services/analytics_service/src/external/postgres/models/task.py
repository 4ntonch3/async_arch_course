import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


table = sa.Table(
    "tasks",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("task_cost_id", sa.Integer, sa.ForeignKey("tasks_costs.id"), nullable=True),
    sa.Column("status", sa.Enum(entities.TaskStatus, name="status"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
)


def build_domain_from_extended_model(model: tuple) -> entities.Task:
    return entities.Task(
        id=str(model[0]),
        public_id=model[1],
        status=model[3],
        created_at=model[4],
        closed_at=model[5],
        cost=entities.TaskCost(
            id=str(model[6]),
            public_id=model[7],
            assign_fee=entities.Money(model[8]),
            completion_award=entities.Money(model[9]),
        ),
    )


def build_domain_from_model(row: tuple, cost: entities.TaskCost | None) -> entities.Task:
    return entities.Task(
        id=str(row[0]),
        public_id=row[1],
        cost=cost,
        status=row[3],
        created_at=row[4],
        closed_at=row[5],
    )
