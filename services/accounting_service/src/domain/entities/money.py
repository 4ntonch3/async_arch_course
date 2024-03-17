from decimal import Decimal


# TODO: enhance
class Money(Decimal):
    def to_decimal(self) -> Decimal:
        return self
