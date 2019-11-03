from django.contrib import admin
from django.urls import path
from django.urls import include

from users.views import *

urlpatterns = [
    path('user/', user_self, name='user_self'),
    path('<int:user_id>/', user_by_id, name='user_by_id'),
    path('search/<str:user_name>/', user_seek_by_name, name='user_seek_by_name'),
    path('<int:user_id>/start_chat/', user_start_chat, name='user_start_chat'),
]
