import uvicorn
from fastapi import FastAPI


def start_api_server(application: FastAPI, host: str, port: int) -> None:
    config = uvicorn.Config(application, host, port)
    api_server = uvicorn.Server(config)

    api_server.run()
