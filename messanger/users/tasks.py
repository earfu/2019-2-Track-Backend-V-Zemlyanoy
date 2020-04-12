from __future__ import absolute_import, unicode_literals

from celery import shared_task
from users.models import User


@shared_task
def add(x,y):
    return x+y

@shared_task
def count_users():
    return User.objects.filter(is_active=True).count()
