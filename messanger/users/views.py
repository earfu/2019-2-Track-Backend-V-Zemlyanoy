from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from chats.models import Chat
from chats.models import Member
from users.forms import UserNewForm
from users.forms import UserLoginForm

from users.serializers import UserSerializer

# Create your views here.
#def login_required(view):
 #   def wrap(*args, **kwargs):
  #      request = args[0]
   #     user = request.user
    #    if user.is_authenticated:
     #       return view(*args, **kwargs)
      #  else:
       #     return redirect('login-user')
    #return wrap

@login_required
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

@login_required
def user_start_chat(request, user_id): # create one-on-one chat
    if request.method == 'GET':
        # add check for user trying to chat with himself
        # then, check for chat already present
        # otherwise, start new chat

        target = User.objects.filter(id=user_id).get()
        user_self = request.user # change to being the initiating user

        chat_obj = Chat(name='test_chat') # look about naming
        chat_obj.save()
        chat_obj.members.add(target)
        chat_obj.members.add(user_self)
        # chat_obj.save()

        return JsonResponse({'New chat': chat_obj.name, 'chat id': chat_obj.id})
    else:
        return HttpResponseNotAllowed(['GET'])

def user_seek_by_name(request, user_name): # search for user by name, exact match only
    findings = User.objects.filter(
        Q(username__contains=user_name) | Q(first_name__contains=user_name) | Q(last_name__contains=user_name)
    )
    try:
        user = findings.get()
        # redirect to user profile
        return JsonResponse({'username': user.username, 'id': user.id})
    except User.MultipleObjectsReturned: # is it possible to have same names at all?
        # display list of found profiles
        return HttpResponse('Placeholder for found user profiles list')
    except User.DoesNotExist:
        return HttpResponse('Placeholder for no such user')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chats/index/')
        else:
            return HttpResponse('Invalid credentials')
    elif request.method == 'GET':
        #return render(request, 'users/login_user.html', {'form': UserLoginForm()})
        return render(request, 'users/login_user.html', {'form': AuthenticationForm()})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def logout_user(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/login/')
    else:
        return HttpResponseNotAllowed(['GET'])

def user_new(request):
    if request.method == 'GET':
        return render(request, 'users/new_user.html', {'form': UserNewForm()})
    elif request.method == 'POST':
        form = UserNewForm(request.POST)
        if form.is_valid():
            #user = User.objects.create_user(form.fields['username'], password=form.fields['password'])
            user = form.save(commit=True)
            return JsonResponse({'User creation:': 'success', 'new user id:': user.id})
        else:
            return JsonResponse({'User creation:': 'invalid form data', 'Errors': list(form.errors.as_data())})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
