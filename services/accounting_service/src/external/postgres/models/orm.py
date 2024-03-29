from datetime import datetime
from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain import entities

from .common import Base


class BillingCycleORM(Base):
    __tablename__ = "billing_cycles"

    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[int] = mapped_column(sa.ForeignKey("workers.id"), nullable=False)
    status: Mapped[entities.BillingCycleStatus] = mapped_column(
        sa.Enum(entities.BillingCycleStatus, name="billing_status"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime(timezone=True), nullable=True)

    transactions: Mapped[list["TransactionORM"]] = relationship(back_populates="billing_cycle")
    worker: Mapped["WorkerORM"] = relationship(back_populates="billing_cycles", lazy="joined")
    payment: Mapped[Optional["PaymentORM"]] = relationship(back_populates="billing_cycle")

    def to_domain(self) -> entities.BillingCycle:
        return entities.BillingCycle(
            id=str(self.id),
            worker=self.worker.to_domain(),
            status=self.status,
            started_at=self.started_at,
            ended_at=self.ended_at,
        )

    def sync_with_domain(self, billing_cycle: entities.BillingCycle) -> None:
        self.status = billing_cycle.status
        self.ended_at = billing_cycle.ended_at


class PaymentORM(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    status: Mapped[entities.PaymentStatus] = mapped_column(
        sa.Enum(entities.PaymentStatus, name="payment_status"), nullable=False
    )
    transaction_id: Mapped[int] = mapped_column(sa.ForeignKey("transactions.id"), nullable=False)
    billing_cycle_id: Mapped[int] = mapped_column(sa.ForeignKey("billing_cycles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    transaction: Mapped["TransactionORM"] = relationship(back_populates="payment", lazy="joined")
    billing_cycle: Mapped["BillingCycleORM"] = relationship(back_populates="payment", lazy="joined")

    def to_domain(self) -> entities.Payment:
        return entities.Payment(
            id=str(self.id),
            public_id=self.public_id,
            billing_cycle=self.billing_cycle.to_domain(),
            transaction=self.transaction.to_domain(),
            status=self.status,
        )

    def sync_with_domain(self, payment: entities.Payment) -> None:
        self.status = payment.status


class TaskCostORM(Base):
    __tablename__ = "tasks_costs"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    assign_fee: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    completion_award: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    task: Mapped["TaskORM"] = relationship(back_populates="task_cost")

    def to_domain(self) -> entities.TaskCost:
        return entities.TaskCost(
            id=str(self.id),
            public_id=self.public_id,
            assign_fee=entities.Money(self.assign_fee),
            completion_award=entities.Money(self.completion_award),
        )


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    task_cost_id: Mapped[int] = mapped_column(sa.ForeignKey("tasks_costs.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    task_cost: Mapped["TaskCostORM"] = relationship(back_populates="task", lazy="joined")

    def to_domain(self) -> entities.Task:
        return entities.Task(
            id=str(self.id),
            public_id=self.public_id,
            cost=self.task_cost.to_domain(),
        )


class TransactionORM(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    worker_id: Mapped[int] = mapped_column(sa.ForeignKey("workers.id"), nullable=False)
    billing_cycle_id: Mapped[int] = mapped_column(sa.ForeignKey("billing_cycles.id"), nullable=False)
    type: Mapped[entities.TransactionType] = mapped_column(
        sa.Enum(entities.TransactionType, name="type"), nullable=False
    )
    credit: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    debit: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(length=256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    payment: Mapped[Optional["PaymentORM"]] = relationship(back_populates="transaction")
    worker: Mapped["WorkerORM"] = relationship(back_populates="transactions")
    billing_cycle: Mapped["BillingCycleORM"] = relationship(back_populates="transactions")

    def to_domain(self) -> entities.Transaction:
        return entities.Transaction(
            id=str(self.id),
            public_id=self.public_id,
            worker=self.worker.to_domain(),
            billing_cycle=self.billing_cycle.to_domain(),
            type=self.type,
            credit=entities.Money(self.credit),
            debit=entities.Money(self.debit),
            description=self.description,
            created_at=self.created_at,
        )


class WorkerORM(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(length=64), nullable=False)
    role: Mapped[entities.WorkerRole] = mapped_column(
        sa.Enum(entities.WorkerRole, name="role"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    transactions: Mapped[list["TransactionORM"]] = relationship(back_populates="worker")
    billing_cycles: Mapped[list["BillingCycleORM"]] = relationship(back_populates="worker")

    def to_domain(self) -> entities.Worker:
        return entities.Worker(
            id=str(self.id),
            public_id=self.public_id,
            balance=entities.Money(self.balance),
            email=self.email,
            role=self.role,
        )

    def sync_with_domain(self, worker: entities.Worker) -> None:
        self.balance = worker.balance
        self.email = worker.email
        self.role = worker.role
