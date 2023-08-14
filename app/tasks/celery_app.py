from celery import Celery

from app.config import RMQ_HOST, RMQ_PASSWORD, RMQ_PORT, RMQ_USER

celery_app = Celery('tasks', broker=f'amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}:{RMQ_PORT}', backend='rpc://')

celery_app.conf.beat_schedule = {
    'test': {
        'task': 'app.tasks.tasks.sync_database_from_xlsx',
        'schedule': 15,
    }
}
celery_app.autodiscover_tasks(['app.tasks.tasks'])
