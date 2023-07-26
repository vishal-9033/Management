import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hotel_Management.settings")

app = Celery("Hotel_Management")

app.config_from_object("django.conf:settings" , namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "send_notification": {
        "task": "send_notification",
        "schedule": crontab(minute="*/1"),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")