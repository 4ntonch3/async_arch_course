from schema_registry import SchemaRegistry

import external
from domain import interfaces, usecases


auth_service_client: external.AuthServiceClient

schema_registry: SchemaRegistry

tasks_repository: interfaces.TasksRepository
workers_repository: interfaces.WorkersRepository
message_broker: interfaces.MessageBroker

apply_deposit_transaction: usecases.ApplyDepositTransactionUsecase
apply_withdrawal_transaction: usecases.ApplyWithdrawalTransactionUsecase
close_billing_cycles: usecases.CloseBillingCyclesUsecase
payout_worker: usecases.PayoutWorkerUsecase
get_worker_balance: usecases.GetWorkerBalanceUsecase
get_worker_transactions: usecases.GetWorkerTransactionsUsecase
get_managers_daily_profit: usecases.GetManagersDailyProfitUsecase
