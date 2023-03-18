import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_sheets_api.settings')

app = Celery('google_sheets_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'Execute every three hours': {
        'task': 'market.tasks.get_exchange_rate_task',
        'schedule': crontab(minute=0, hour='*/3'),
    },
    'Execute every afternoon': {
        'task': 'market.tasks.send_notification',
        'schedule': crontab(minute=0, hour='12'),
    },     
}

