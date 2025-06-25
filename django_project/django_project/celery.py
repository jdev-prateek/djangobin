from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# set the default Django settings module for the 'celery' program.
# if os.environ.get('DJANGO_SETTINGS_MODULE'):
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings.dev')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings.prod')
#
#
# print(os.environ.get('DJANGO_SETTINGS_MODULE'))
# from _datetime import datetime
# print(datetime.now())

app = Celery('djangobin')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove-snippets-daily-at-midnight': {
        'task': 'djangobin.tasks.remove_snippets',
        'schedule': crontab(minute=0, hour=0),
    },
}