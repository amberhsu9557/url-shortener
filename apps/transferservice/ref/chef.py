from celery import Celery

CELERY_BROKER_URL = "redis://redis:redis@redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:redis@redis:6379"
# app = Celery(__name__,broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND, include=['test_celery.tasks'])
# app = Celery(__name__,broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND, include=['crawler.tasks'])
app = Celery(__name__,broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND)
app.conf.timezone = 'Asia/Taipei'

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

app.conf.update(
    result_expires=864000,
    task_routes = {
        '.tasks.add': {'queue': 'crawler'},
    },
)