from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

#taskqueue = Celery('messanger', broker='redis://redis:6379/0', backend='redis://redis:6379/0', include=['messanger.tasks.tasks'])
#taskqueue = Celery('messanger')
#taskqueue.config_from_object(settings, namespace='CELERY')
#taskqueue.conf.update(result_expires=3600, include=['messanger.tasks.tasks'])

#if __name__ == '__main__':
 #   taskqueue.start()
#taskqueue.start()
