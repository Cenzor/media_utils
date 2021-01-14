import os
from celery import Celery
# from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_utils.settings')
app = Celery('media_utils')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Vladivostok'

# app.conf.beat_schedule = {
#     'send-report-every-single-minute': {
#         'task': 'publish.tasks.send_view_count_report',
#         'schedule': crontab(hour=22, minute=36),
#     },
# }

