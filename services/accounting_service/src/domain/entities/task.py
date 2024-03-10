import random
from dataclasses import dataclass

from .money import Money


@dataclass
class Task:
    id: str
    public_id: str
    assign_fee: Money
    completion_award: Money

    @staticmethod
    def calculate_assign_fee() -> Money:
        return Money(random.randint(10, 20))

    @staticmethod
    def calculate_completion_award() -> Money:
        return Money(random.randint(20, 40))
