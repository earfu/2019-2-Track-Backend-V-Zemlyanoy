from __future__ import absolute_import, unicode_literals
from string import Template as str_Template

from celery import shared_task

from django.core.mail import send_mail

@shared_task
def chat_mail_note(username, chat_name, target_mail):
    send_mail(
        'You created a new chat',
        str_Template(
            'Hello $username,\n\n you have created a new chat named $chat'
        ).substitute(username=username, chat=chat_name),
        'from@no.one',
        [target_mail]
    )

