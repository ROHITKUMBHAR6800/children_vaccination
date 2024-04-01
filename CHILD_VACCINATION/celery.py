from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CHILD_VACCINATION.settings')
from celery.schedules import crontab

app = Celery('CHILD_VACCINATION')

app.conf.enable_utc = False

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(timezon = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

#Celery Beat Settings
# to run taskt for any specific time interval
app.conf.beat_schedule = {
    'add-every-day' :{
        'task': 'op_send_email_notification',
        'schedule' : crontab(minute='*/1')
    }

    # 'send-email-every-day': {
    #     'task': 'path.to.your.task.function',
    #     'schedule': crontab(hour=0, minute=0),  # This will run the task at midnight every day
    # },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')