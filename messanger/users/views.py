from django.shortcuts import render

from django.http import JsonResponse

# Create your views here.

def user_self(request):
    if request.method == 'GET':
        return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s own profile', })
    else:
        raise Http405

def user_by_id(request, user_id):
    if request.method == 'GET':
        return JsonResponse({'App': 'users', 'Placeholder_for': 'user\'s profile', 'user_id': user_id, })
    else:
        raise Http405
