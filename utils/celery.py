import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.conf.update(
    include=[
        "apps.images_app.tasks",
    ],
)

app.conf.beat_schedule = {
    "deletar-imgs-a-cada-365-dias": {
        "task": "apps.images_app.tasks.cleanup_images",
        "schedule": crontab(minute=1, hour="*/12"),
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
