from fastapi import FastAPI

from domain import interfaces, usecases
from external import AuthServiceClient, broker

from . import dependency, routes


def create_web_app(
    auth_service_client: AuthServiceClient,
    tasks_repository: interfaces.TasksRepository,
    workers_repository: interfaces.WorkersRepository,
    message_broker: interfaces.MessageBroker,
    apply_enroll_transaction: usecases.ApplyEnrollTransactionUsecase,
    apply_withdraw_transaction: usecases.ApplyWithdrawTransactionUsecase,
    close_billing_cycles: usecases.CloseBillingCyclesUsecase,
    worker_payout: usecases.WorkerPayoutUsecase,
    get_worker_balance: usecases.GetWorkerBalanceUsecase,
    get_worker_transactions: usecases.GetWorkerTransactionsUsecase,
    get_managers_daily_profit: usecases.GetManagersDailyProfitUsecase,
) -> FastAPI:
    dependency.auth_service_client = auth_service_client

    dependency.tasks_repository = tasks_repository
    dependency.workers_repository = workers_repository
    dependency.message_broker = message_broker

    dependency.apply_enroll_transaction = apply_enroll_transaction
    dependency.apply_withdraw_transaction = apply_withdraw_transaction
    dependency.close_billing_cycles = close_billing_cycles
    dependency.worker_payout = worker_payout
    dependency.get_worker_balance = get_worker_balance
    dependency.get_worker_transactions = get_worker_transactions
    dependency.get_managers_daily_profit = get_managers_daily_profit

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        on_startup=(broker.start,),
        on_shutdown=(broker.close,),
    )

    app.include_router(routes.billing_cycles_router)
    app.include_router(routes.developer_router)
    app.include_router(routes.manager_router)

    return app
