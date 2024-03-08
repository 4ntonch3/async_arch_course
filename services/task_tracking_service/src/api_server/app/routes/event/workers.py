from api_server.app import dependency
from external import broker

from . import models


_CUD_WORKERS_EVENT_TOPIC = "worker-stream"


@broker.subscriber(_CUD_WORKERS_EVENT_TOPIC)
async def handle_worker_created(event: dict) -> None:
    event_title = event.get("title")

    if event_title != models.WorkerCreatedEvent.EVENT_TITLE:
        return

    worker_created_event = models.WorkerCreatedEvent.model_validate(event)
    worker_data = worker_created_event.payload

    await dependency.add_worker.execute(worker_data.worker_id, worker_data.role)
