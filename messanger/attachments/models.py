from django.db import models

# Create your models here.


class Attachment(models.Model):
    name = models.CharField(max_length = 30, blank=True)
    attachment = models.FileField()
