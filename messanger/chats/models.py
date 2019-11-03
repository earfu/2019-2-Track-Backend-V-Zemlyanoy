from django.db import models

from users.models import User

# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length = 30, blank=True)
    members = models.ManyToManyField(User, through='Member')

class Member(models.Model): # needs no own serial key, but can it be removed?
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    last_read_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta: # ???
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'chat_id'], name='unique_membership'),
        ]

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # make default 'Unknown' user?
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
