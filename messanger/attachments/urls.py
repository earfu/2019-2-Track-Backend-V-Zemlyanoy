from django.contrib import admin
from django.urls import path
from django.urls import include

from attachments.views import *

urlpatterns = [
    path('attach/', attach, name='attach'),
]
