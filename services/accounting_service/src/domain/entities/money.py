from decimal import Decimal


class Money(Decimal):
    def to_decimal(self) -> Decimal:
        return self
