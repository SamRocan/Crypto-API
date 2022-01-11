import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULES', 'cryptoApi.settings')

app = Celery('cryptoApi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

