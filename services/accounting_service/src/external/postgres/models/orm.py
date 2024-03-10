from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain import entities

from .common import Base


class BillingCycleORM(Base):
    __tablename__ = "billing_cycles"

    class Status(StrEnum):
        OPEN = "open"
        CLOSE = "close"

    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[int] = mapped_column(sa.ForeignKey("workers.id"), nullable=False)
    status: Mapped[Status] = mapped_column(sa.Enum(Status, name="billing_status"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime(timezone=True), nullable=True)

    transactions: Mapped[list["TransactionORM"]] = relationship(back_populates="billing_cycle")
    worker: Mapped["WorkerORM"] = relationship(back_populates="billing_cycles", lazy="joined")
    payment: Mapped[Optional["PaymentORM"]] = relationship(back_populates="billing_cycle")

    def to_domain(self) -> entities.BillingCycle:
        return entities.BillingCycle(
            id=str(self.id),
            worker=self.worker.to_domain(),
            status=entities.BillingCycleStatus(str(self.status)),
            started_at=self.started_at,
            ended_at=self.ended_at,
        )

    def sync_with_domain(self, billing_cycle: entities.BillingCycle) -> None:
        self.status = self.Status(str(billing_cycle.status))
        self.ended_at = billing_cycle.ended_at


class PaymentORM(Base):
    __tablename__ = "payments"

    class Status(StrEnum):
        CREATED = "created"
        IN_PROGRESS = "in_progress"
        FAILED = "failed"
        PROCESSED = "processed"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    status: Mapped[Status] = mapped_column(sa.Enum(Status, name="payment_status"), nullable=False)
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
            status=entities.PaymentStatus(str(self.status)),
        )

    def sync_with_domain(self, payment: entities.Payment) -> None:
        self.status = self.Status(str(payment.status))


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    assign_fee: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    completion_award: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    def to_domain(self) -> entities.Task:
        return entities.Task(
            id=str(self.id),
            public_id=self.public_id,
            assign_fee=entities.Money(self.assign_fee),
            completion_award=entities.Money(self.completion_award),
        )


class TransactionORM(Base):
    __tablename__ = "transactions"

    class Type(StrEnum):
        ENROLL = "enroll"
        WITHDRAW = "withdraw"
        PAYMENT = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    worker_id: Mapped[int] = mapped_column(sa.ForeignKey("workers.id"), nullable=False)
    billing_cycle_id: Mapped[int] = mapped_column(sa.ForeignKey("billing_cycles.id"), nullable=False)
    type: Mapped[Type] = mapped_column(sa.Enum(Type, name="type"), nullable=False)
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
            type=entities.TransactionType(str(self.type)),
            credit=entities.Money(self.credit),
            debit=entities.Money(self.debit),
            description=self.description,
            created_at=self.created_at,
        )


class WorkerORM(Base):
    __tablename__ = "workers"

    class Role(StrEnum):
        ADMINISTATOR = "administrator"
        ACCOUNTANT = "accountant"
        DEVELOPER = "developer"
        MANAGER = "manager"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(sa.String(length=64), unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=3), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(length=64), nullable=False)
    role: Mapped[Role] = mapped_column(sa.Enum(Role, name="role"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)

    transactions: Mapped[list["TransactionORM"]] = relationship(back_populates="worker")
    billing_cycles: Mapped[list["BillingCycleORM"]] = relationship(back_populates="worker")

    def to_domain(self) -> entities.Worker:
        return entities.Worker(
            id=str(self.id),
            public_id=self.public_id,
            balance=entities.Money(self.balance),
            email=self.email,
            role=entities.WorkerRole(str(self.role)),
        )

    def sync_with_domain(self, worker: entities.Worker) -> None:
        self.balance = worker.balance
        self.email = worker.email
        self.role = self.Role(str(worker.role))
