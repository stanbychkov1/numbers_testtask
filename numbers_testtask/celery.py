import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numbers_testtask.settings')

app = Celery('numbers_testtask')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


