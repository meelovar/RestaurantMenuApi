import asyncio

from app.config import XLSX_PATH
from app.services.admin import AdminService
from app.tasks.celery_app import celery_app


@celery_app.task
def sync_database_from_xlsx() -> None:
    loop = asyncio.get_event_loop()
    service = AdminService(XLSX_PATH)

    loop.run_until_complete(service.execute())
