"""initial

Revision ID: 78cea44fb262
Revises: 
Create Date: 2024-03-15 23:06:54.349908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78cea44fb262'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks_costs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=64), nullable=False),
    sa.Column('assign_fee', sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column('completion_award', sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=64), nullable=False),
    sa.Column('balance', sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('role', sa.Enum('ADMINISTATOR', 'ACCOUNTANT', 'DEVELOPER', 'MANAGER', name='role'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('billing_cycles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSE', name='billing_status'), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=64), nullable=False),
    sa.Column('task_cost_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['task_cost_id'], ['tasks_costs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=64), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('billing_cycle_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('DEPOSIT', 'WITHDRAWAL', 'PAYMENT', name='type'), nullable=False),
    sa.Column('credit', sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column('debit', sa.Numeric(precision=8, scale=3), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['billing_cycle_id'], ['billing_cycles.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=64), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'IN_PROGRESS', 'FAILED', 'PROCESSED', name='payment_status'), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('billing_cycle_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['billing_cycle_id'], ['billing_cycles.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('transactions')
    op.drop_table('tasks')
    op.drop_table('billing_cycles')
    op.drop_table('workers')
    op.drop_table('tasks_costs')
    # ### end Alembic commands ###
