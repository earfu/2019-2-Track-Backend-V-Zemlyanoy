from django.db import models

from chats.models import Message

# Create your models here.


class Attachment(models.Model):
    name = models.CharField(max_length = 50, blank=True)
    attachment = models.FileField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
