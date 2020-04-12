import json
import jwt

import cent

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from users.models import User
from chats.models import Chat, Message
from chats.forms import MessageSendForm, ChatCreateForm
from attachments.views import attach
from attachments.models import Attachment
from users.views import login_required_unless_options

from chats.serializers import ChatSerializer, MessageSerializer
from chats.tasks import chat_mail_note

# Create your views here.

cent_client = cent.Client(settings.CENTRIFUGO_ADDRESS, api_key=settings.CENTRIFUGO_API_KEY, timeout=4)

@login_required
def index(request): # display chat list for current user
    if request.method == 'GET':
        user = request.user # change to user's self later
        chat_list = Chat.objects.filter(member__user_id=user.id).values('id', 'name')

        # generate centrifugo HMAC token
        cent_token = jwt.encode(
            {'sub': str(user.id)},
            settings.CENTRIFUGO_TOKEN_HMAC_SECRET_KEY,
            algorithm='HS256'
        ).decode()
        response = JsonResponse({'App': 'chats',
            'user_id': user.id,
            'username': user.username,
            'chats': list(chat_list),
            'cent_token': cent_token
        })
        try:
            response['Access-Control-Allow-Origin'] = request.headers['Origin']
            response['Access-Control-Allow-Credentials'] = 'true'
        except KeyError:
            pass
        return response
    #elif request.method == 'OPTIONS':
     #   response = HttpResponse('', status=200)
      #  response['Access-Control-Allow-Origin'] = request.headers['Origin']
       # response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        #response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, X-CSRFToken'
        #response['Access-Control-Allow-Credentials'] = 'true'
        #return response
    else:
        return HttpResponseNotAllowed(['GET', 'OPTIONS'])

@cache_page(60*15)
@login_required
def chat_messages(request, chat_id): # display chat messages list
    if request.method == 'GET':
        user = request.user
        try:
            chat = Chat.objects.filter(id=chat_id, member__user_id=user.id).get()
            response = JsonResponse({
                'App': 'chats',
                'chat_id': chat_id,
                'chat_name': chat.name,
                'username': user.username,
                'messages':
                    list(Message.objects
                        .filter(chat_id=chat_id)
                        .values('id', 'user__username', 'content', 'added_at')
                        .order_by('added_at')
                    )
            })
        except Chat.DoesNotExist:
            response = JsonResponse({
                'error': 'Either chat does not exist, or you are not a member'
                })
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Vary'] = 'Origin'
        return response
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required
def chat_read_message(request, chat_id, message_id): # display message text
    if request.method == 'GET':
        user = request.user # for now
        try:
            chat = Chat.objects.filter(id=chat_id).filter(member__user_id=user.id).get()
            message = Message.objects.filter(id=message_id, chat_id=chat.id).get()
            return JsonResponse({
                'App': 'chats',
                'Placeholder_for': 'message display',
                'chat_id': chat_id,
                'message_id': message_id,
                'message text': message.content,
                'message attachments:': list(message.attachment_set.values('id')),
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

@login_required
def chat_detail(request, chat_id): # display member list of chat
    if request.method == 'GET':
        user = request.user # for now
        try:
            chat = Chat.objects.filter(id=chat_id).filter(member__user_id=user.id).get()
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

@login_required_unless_options
def create_chat(request): # not used yet
    if request.method == 'GET':
        return HttpResponse('Here be general chat creation page?')
    elif request.method == 'POST':
        user = request.user
        if request.is_ajax():
            form = ChatCreateForm({'name': json.loads(request.body)['chatName']})
        else:
            form = ChatCreateForm(request.POST)
        if form.is_valid():
            chat = form.save()
            chat.members.add(user)
            response = JsonResponse({'Chat creation': 'success', 'chat id': chat.id})
            try:
                cent_client.publish('chats#' + str(user.id), {'id': chat.id, 'name': chat.name})
            except cent.CentException:
                pass
            if (user.email is not None):
                chat_mail_note(user.username, chat.name, user.email)

        else:
            response = JsonResponse({'Chat creation': 'invalid form', })
        if request.is_ajax():
            response['Access-Control-Allow-Origin'] = request.headers['Origin']
            response['Access-Control-Allow-Credentials'] = 'true'
        return response
    elif request.method == 'OPTIONS':
        response = HttpResponse('', status=200)
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Headers'] = 'X-CSRFToken, X-Requested-With'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'OPTIONS'])

def default_index(request): # the default server page
    if request.method == 'GET':
        return render(request, 'index.html')
#    elif request.method == 'POST':
#        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required_unless_options
#@csrf_exempt
def chat_send_message(request, chat_id):
    if request.method == 'POST':
        #user = User.objects.filter(id=1).get()
        user = request.user
        msg = Message(user_id=user.id, chat_id=chat_id)
        if request.POST:
            form = MessageSendForm(request.POST, instance=msg)
        else:
            form = MessageSendForm({'content': json.loads(request.body)['content']}, instance=msg)
        if form.is_valid():
            form.save(commit=True)
            response = JsonResponse({'Post message': 'success', 'Message id': msg.id})
            try:
                cent_client.publish('$chat'+str(chat_id), {
                    'id': msg.id,
                    'user__username': user.username,
                    'content': msg.content,
                    'added_at': str(msg.added_at)
                })
            except cent.CentException:
                pass
        else:
            response = JsonResponse({'Post message': 'invalid form'})
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    elif request.method == 'GET':
        return render(request, 'chats/send_message.html', {'form': MessageSendForm(), 'chat_id': chat_id})
    elif request.method == 'OPTIONS':
        response = HttpResponse('', status=200)
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Headers'] = 'X-CSRFToken'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'OPTIONS'])


#class Rest_Chat_List(APIView):
 #   serializer_class = ChatSerializer
  #  def get_queryset(self):
   #     return Chat.objects.filter(member__user_id=self.request.user.id).all()
   # def get(self, request):
    #    return Response({'chats': serializer.data})

class ChatViewSet(ModelViewSet):

    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(member__user_id=self.request.user.id).all().order_by('id')

    def retrieve(self, request, pk=None):
        try:
            queryset = Chat.objects.filter(member__user_id=self.request.user.id, id=pk).get()
        except Chat.DoesNotExist:
            return Response({'Chat detail': 'No such chat, or you are not a member'}, status=404)
        except ValueError:
            return Response({'Chat detail': 'Wrong value for chat id'}, status=404)
        serializer = self.serializer_class(queryset)
       # serializer.build_relational_field('messages', ('','',True,'Message'))
        return Response(serializer.data)

class MessageViewSet(ModelViewSet):

    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chat__member__user_id=self.request.user.id).all().order_by('added_at')

    @action(methods=['GET'], detail=True, url_path='all')
    def chat_list(self, request, pk=None):
        if pk is None:
            #return Response(self.serializer_class(self.get_queryset(), many=True).data)
            return Response({'Chat message list': 'No chat specified'}, status=404)
        else:
            try:
                chat = Chat.objects.filter(id=pk).get()
                chat.members.filter(id=request.user.id).get()
            except User.DoesNotExist:
                return Response({'Chat message list': 'No such chat, or you are not a member'}, status=404)
            except Chat.DoesNotExist:
                return Response({'Chat message list': 'No such chat, or you are not a member'}, status=404)

            queryset = Message.objects.filter(chat_id=pk).all().order_by('added_at')
            serializer = self.serializer_class(queryset,many=True)
            return Response(serializer.data)

@csrf_exempt # could private subscriptions be stolen?
@login_required_unless_options
def cent_subscribe(request): # required for centrifuge-js private channels
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        tokens = []
        clientID = data['client']
        for channel in data['channels']:
            if (channel.rsplit('$chat')[1].isnumeric()): # case of chat subscription
                chat_id = int(channel.rsplit('$chat')[1])
                try:
                    chat = Chat.objects.filter(id=chat_id, member__user_id=user.id).get()
                    tokens.append({
                        'channel': channel,
                        'token': jwt.encode(
                            {'client': clientID, 'channel': channel},
                            settings.CENTRIFUGO_TOKEN_HMAC_SECRET_KEY,
                            algorithm='HS256'
                        ).decode() # and this is the correct one
                        })
                except Chat.DoesNotExist:
                    pass
        response = JsonResponse({'channels': tokens, 'clientID': clientID})
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    elif request.method == 'OPTIONS':
        response = HttpResponse('', status=200)
        response['Access-Control-Allow-Method'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
        response['Access-Control-Allow-Origin'] = request.headers['Origin']
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return HttpResponseNotAllowed(['POST', 'OPTIONS'])
