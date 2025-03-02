import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_celery.settings")

app = Celery("library_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
