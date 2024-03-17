import sqlalchemy as sa

from domain import entities

from ..common import metadata_obj


table = sa.Table(
    "transactions",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("public_id", sa.String(length=64), unique=True, nullable=False),
    sa.Column("type", sa.Enum(entities.TransactionType, name="type"), nullable=False),
    sa.Column("value", sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)


def build_domain_from_model(row: tuple) -> entities.Transaction:
    return entities.Transaction(
        id=str(row[0]),
        public_id=row[1],
        type=entities.TransactionType(str(row[2])),
        value=entities.Money(row[3]),
        created_at=row[4],
    )
