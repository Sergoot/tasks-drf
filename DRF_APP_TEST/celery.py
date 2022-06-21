import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_APP_TEST.settings')

app = Celery('DRF_APP_TEST')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
