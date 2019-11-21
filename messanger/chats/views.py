from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from users.models import User
from chats.models import Chat
from chats.models import Message
from chats.forms import MessageSendForm
from chats.forms import ChatCreateForm

# Create your views here.

def index(request): # display chat list for current user
    if request.method == 'GET':
        user = User.objects.filter(username='useradm').get() # change to user's self later
        chat_list = Chat.objects.filter(member__user_id=user.id).values('id', 'name')
        # then display chat list
        return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat list screen',
            'user_self': user.username, 'chats': list(chat_list)})
    else:
        return HttpResponseNotAllowed(['GET'])

def chat_messages(request, chat_id): # display chat messages list
    if request.method == 'GET':
        user_id = 1 # for now
        try:
            chat = Chat.objects.filter(id=chat_id, member__user_id=user_id).get()
            return JsonResponse({
                'App': 'chats',
                'Placeholder_for': 'chat screen',
                'chat_id': chat_id,
                'messages': list(Message.objects.filter(chat_id=chat_id).values('id', 'user')) # no date, no content
            })
        except Chat.DoesNotExist:
            return JsonResponse({
                'Response for chat request': 'Either chat does not exist, or you are not a member'
                })
    else:
        return HttpResponseNotAllowed(['GET'])

def chat_read_message(request, chat_id, message_id): # display message text
    if request.method == 'GET':
        user_id = 1 # for now
        try:
            chat = Chat.objects.filter(id=chat_id).filter(member__user_id=user_id).get()
            message = Message.objects.filter(id=message_id, chat_id=chat.id).get()
            return JsonResponse({
                'App': 'chats',
                'Placeholder_for': 'message display',
                'chat_id': chat_id,
                'message_id': message_id,
                'message text': message.content,
            })
        except Message.DoesNotExist:
            return JsonResponse({
                'Response for message request': 'Either message does not exist, or is not in this chat'
                })
        except Chat.DoesNotExist:
            return JsonResponse({
                'Response for message request': 'Either chat does not exist, or you are not in this chat'
                })

    else:
        return HttpResponseNotAllowed(['GET'])


def chat_detail(request, chat_id): # display member list of chat
    if request.method == 'GET':
        user_id = 1 # for now
        try:
            chat = Chat.objects.filter(id=chat_id).filter(member__user_id=user_id).get()
            return JsonResponse({
                'App': 'chats',
                'Placeholder_for': 'chat details screen',
                'chat_id': chat_id,
                'members': list(chat.members.filter().values('id', 'username'))
            })
        except Chat.DoesNotExist:
            return JsonResponse({
                'Response for chat detail request': 'Either chat does not exist, or you are not a member'
                })
    else:
        return HttpResponseNotAllowed(['GET'])

def create_chat(request): # not used yet
    if request.method == 'GET':
        return HttpResponse('Here be general chat creation page?')
    elif request.method == 'POST':
        user = User.objects.filter(id=1).get() # for now
        form = ChatCreateForm(request.POST)
        if form.is_valid():
            chat = form.save()
            chat.members.add(user)
            return JsonResponse({'Chat creation': 'success', 'chat id': chat.id})
        else:
            return JsonResponse({'Chat creation': 'invalid form', })
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def default_index(request): # the default server page
    if request.method == 'GET':
        return render(request, 'index.html')
#    elif request.method == 'POST':
#        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed(['GET'])

def chat_send_message(request, chat_id):
    if request.method == 'POST':
        user_id = 1 # for now
        msg = Message(user_id=user_id, chat_id=chat_id)
        form = MessageSendForm(request.POST, instance=msg)
        if form.is_valid():
            form.save(commit=True)
            return JsonResponse({'Message sending result': 'success', 'Message id': msg.id})
        else:
            return JsonResponse({'Message sending result': 'invalid form'})
    elif request.method == 'GET':
        return JsonResponse({
            'Message sending page': 'Sorry, no html form here',
            'What to do': 'Send POST request some other way'
            })
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
