import abc


class EmailClient(abc.ABC):
    @abc.abstractmethod
    async def send(self, email_address: str, message: str) -> None:
        pass
