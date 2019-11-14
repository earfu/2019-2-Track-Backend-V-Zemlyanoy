from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from users.models import User
from chats.models import Chat

# Create your views here.

def index(request):
    if request.method == 'GET':
        user = User.objects.filter(username='useradm').get() # change to user's self later
        chat_list = Chat.objects.filter(member__user_id=user.id).values('id')
        # then display chat list
        return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat list screen',
            'user_self': user.username, 'chats': list(chat_list)})
    else:
        return HttpResponseNotAllowed(['GET'])


def chat_detail(request, chat_id):
    if request.method == 'GET':
        user_id = 1 # for now
        try:
            chat = Chat.objects.filter(id=chat_id).filter(member__user_id=user_id).get()
            return JsonResponse({
                'App': 'chats',
                'Placeholder_for': 'chat screen',
                'chat_id': chat_id,
                'members': list(chat.members.filter().values('id', 'username'))
            })
        except Chat.DoesNotExist:
            return JsonResponse({
                'Response for chat detail request': 'Either chat does not exist, or you are not a member'
                })
    else:
        return HttpResponseNotAllowed(['GET'])

def create_chat(request):
    if request.method == 'GET':
        return HttpResponse('Here be general chat creation page?')
    else:
        return HttpResponseNotAllowed(['GET'])

def default_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
#    elif request.method == 'POST':
#        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed(['GET'])
