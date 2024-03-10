from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .worker import Worker


class BillingCycleStatus(StrEnum):
    OPEN = "open"
    CLOSE = "close"


@dataclass
class BillingCycle:
    id: str
    worker: Worker
    status: BillingCycleStatus
    started_at: datetime
    ended_at: datetime | None

    def close(self) -> None:
        self.status = BillingCycleStatus.CLOSE
        self.ended_at = datetime.utcnow()
