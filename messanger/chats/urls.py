from django.contrib import admin
from django.urls import path
from django.urls import include

from chats.views import *

urlpatterns = [
    path('index/', index, name='chats-index'),
    path('<int:chat_id>/detail/', chat_detail, name='chat_detail'), # but really, name is unnecessary for now
    path('<int:chat_id>/', chat_messages, name='chat_messages'),
    path('<int:chat_id>/message/<int:message_id>/', chat_read_message, name='chat_read_message'),
    path('create_chat/', create_chat, name='create_chat'),
    path('<int:chat_id>/send_message/', chat_send_message, name='chat_send_message'),
]
