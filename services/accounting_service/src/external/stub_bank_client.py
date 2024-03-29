from domain import entities, interfaces
from logger import LOGGER


class StubBankClient(interfaces.BankClient):
    async def transfer(self, worker_public_id: str, value: entities.Money) -> None:
        msg_info = f"Bank transfer is done. Worker ID: {worker_public_id}. Value: {value}."
        LOGGER.info(msg_info)
