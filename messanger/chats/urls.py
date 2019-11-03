from django.contrib import admin
from django.urls import path
from django.urls import include

from chats.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'), # but really, name is unnecessary for now
    path('create_chat/', create_chat, name='create_chat'),
]
