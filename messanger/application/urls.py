"""messanger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout

from rest_framework import routers

from chats.views import default_index, ChatViewSet, MessageViewSet
from users.views import UserViewSet
from users.views import login_user, logout_user

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login-user'),
    path('logout/', logout_user, name='logout-user'),
    path('index/', default_index), # should not be in chats urls file
    path('chats/', include('chats.urls')),
    path('contacts/', include('contacts.urls')),
    path('users/', include('users.urls')),
    path('attachments/', include('attachments.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # DRF login/logout
    path('api/', include(router.urls)), # all DRF default routing
#    path('api/chats/', Rest_Chat_List.as_view())
]

urlpatterns += [
    path('captcha/', include('captcha.urls'), name='captcha'),
]
