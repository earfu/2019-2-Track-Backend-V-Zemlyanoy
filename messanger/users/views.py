from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from users.models import User
from chats.models import Chat
from chats.models import Member

# Create your views here.

def user_self(request): # display user's own profile
    if request.method == 'GET':
        return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s own profile', })
    else:
        return HttpResponseNotAllowed(['GET'])

def user_by_id(request, user_id): # display user by id
    if request.method == 'GET':
        target = User.objects.filter(id=user_id).values('id', 'username')
        try:
            return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s profile', 'user_id': user_id,
                'user': target[0]
            })
        except IndexError:
            return JsonResponse({'User search result': 'No such user found'})

    else:
        return HttpResponseNotAllowed(['GET'])

def user_start_chat(request, user_id): # create one-on-one chat
    if request.method == 'GET':
        # add check for user trying to chat with himself
        # then, check for chat already present
        # otherwise, start new chat

        target = User.objects.filter(id=user_id).get()
        user_self = User.objects.filter(id=1).get() # change to being the initiating user

        chat_obj = Chat(name='test_chat') # look about naming
        chat_obj.save()
        chat_obj.members.add(target)
        chat_obj.members.add(user_self)
        # chat_obj.save()

        return JsonResponse({'New chat': chat_obj.name, 'chat id': chat_obj.id})
    else:
        return HttpResponseNotAllowed(['GET'])

def user_seek_by_name(request, user_name): # search for user by name, exact match only
    findings = User.objects.filter(username=user_name)
    try:
        user = findings.get()
        # redirect to user profile
        return HttpResponse('Placeholder for found user profile')
    except User.MultipleObjectsReturned: # is it possible to have same names at all?
        # display list of found profiles
        return HttpResponse('Placeholder for found user profiles list')
    except User.DoesNotExist:
        return HttpResponse('Placeholder for no such user')

