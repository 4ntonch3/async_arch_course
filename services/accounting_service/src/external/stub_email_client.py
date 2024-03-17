from domain import interfaces
from logger import LOGGER


class StubEmailClient(interfaces.EmailClient):
    async def send(self, email_address: str, message: str) -> None:
        msg_info = f"Email is sent. Address: {email_address}. Message: {message}."
        LOGGER.info(msg_info)
