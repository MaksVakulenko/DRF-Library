import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_transport_options = {'broker_connection_retry_on_startup': True}
app.conf.beat_schedule = {
    'cancel_unpaid_borrowings_every_minute': {
        'task': 'payment.tasks.auto_cancel_unpaid_borrowings',
        'schedule': crontab(minute='*'),  # Виконується кожну хвилину
    },
}