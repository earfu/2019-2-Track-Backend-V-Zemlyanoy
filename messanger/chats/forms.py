from django.forms import ModelForm
from chats.models import Message
from chats.models import Chat

class MessageSendForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ChatCreateForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['name']
