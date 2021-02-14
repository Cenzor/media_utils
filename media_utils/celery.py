import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_utils.settings')
app = Celery('media_utils')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Vladivostok'
