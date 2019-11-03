from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from users.models import User
from chats.models import Chat

# Create your views here.

def index(request):
    if request.method == 'GET':
        user = User.objects.filter(username='useradm').get() # change to user's self
        chat_list = Chat.objects.filter(member__user_id=user.id)
        # then display chat list
        return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat list screen', 'user_self': user.username})
    else:
        return HttpResponseNotAllowed(['GET'])


def chat_detail(request, chat_id):
    if request.method == 'GET':
        return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat screen', 'chat_id': chat_id, })
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
