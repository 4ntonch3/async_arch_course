from api_server.app import dependency
from external import broker

from . import models


_CUD_WORKERS_EVENT_TOPIC = "workers-stream"


@broker.subscriber(_CUD_WORKERS_EVENT_TOPIC)
async def handle_new_worker(event: dict) -> None:
    event_title = event.get("title")

    if event_title != models.WorkerAddedEvent.EVENT_TITLE:
        return

    worker_added_event = models.WorkerAddedEvent.model_validate(event)

    await dependency.add_worker.execute(worker_added_event.id, worker_added_event.role)
