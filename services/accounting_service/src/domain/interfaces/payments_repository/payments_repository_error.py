class PaymentsRepositoryError(Exception):
    pass


class PaymentAlreadyProcessedError(PaymentsRepositoryError):
    pass
