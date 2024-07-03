from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CHILD_VACCINATION.settings')

app = Celery('CHILD_VACCINATION')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)
#Celery Beat Settings
app.conf.beat_schedule = {
    'VACCINATION-REMINDER-DAILY-NOTIFICATION-MAIL' :{
        'task': 'PRIMARY_HEALTH_CENTER.tasks.vaccination_notification',
        'schedule' : crontab(hour=22, minute=20)
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')