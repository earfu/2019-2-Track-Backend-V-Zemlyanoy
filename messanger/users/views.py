from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from users.models import User
from chats.models import Chat
from chats.models import Member

# Create your views here.

def user_self(request):
    if request.method == 'GET':
        return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s own profile', })
    else:
        return HttpResponseNotAllowed(['GET'])

def user_by_id(request, user_id):
    if request.method == 'GET':
        return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s profile', 'user_id': user_id, })
    else:
        return HttpResponseNotAllowed(['GET'])

def user_start_chat(request, user_id):
    if request.method == 'GET':
        # add check for user trying to chat with himself
        # then, check for chat already present
        # otherwise, start new chat

        target = User.objects.filter(pk=user_id).get()
        user_self = User.objects.filter(pk=1).get() # change to being the initiating user

        chat_obj = Chat(name='test_chat') # look about naming
        chat_obj.save()
        chat_obj.members.add(target)
        chat_obj.members.add(user_self)
        # chat_obj.save()

        return HttpResponse('Placeholder response for new chat being started')
    else:
        return HttpResponseNotAllowed(['GET'])

def user_seek_by_name(request, user_name):
    findings = User.objects.filter(username=user_name)
    try:
        user = findings.get()
        # redirect to user profile
        return HttpResponse('Placeholder for found user profile')
    except User.MultipleObjectsReturned:
        # display list of found profiles
        return HttpResponse('Placeholder for found user profiles list')
    except User.DoesNotExist:
        return HttpResponse('Placeholder for no such user')

