import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'send_mail_every_week': {
        'task': 'news.tasks.week_send_email_task',
        'schedule': crontab(hour='8', minute='0', day_of_week='mon'),

    }
}
app.autodiscover_tasks()