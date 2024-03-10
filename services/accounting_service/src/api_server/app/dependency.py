import external
from domain import interfaces, usecases


auth_service_client: external.AuthServiceClient

tasks_repository: interfaces.TasksRepository
workers_repository: interfaces.WorkersRepository
message_broker: interfaces.MessageBroker

apply_enroll_transaction: usecases.ApplyEnrollTransactionUsecase
apply_withdraw_transaction: usecases.ApplyWithdrawTransactionUsecase
close_billing_cycles: usecases.CloseBillingCyclesUsecase
worker_payout: usecases.WorkerPayoutUsecase
get_worker_balance: usecases.GetWorkerBalanceUsecase
get_worker_transactions: usecases.GetWorkerTransactionsUsecase
get_managers_daily_profit: usecases.GetManagersDailyProfitUsecase
