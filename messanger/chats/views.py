from django.shortcuts import render

from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.method == 'GET':
        return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat screen',})
#    elif request.method == 'POST':
#        return render(request, 'index.html')
    else:
        raise Http405


def chat_detail(request, chat_id):
    return JsonResponse({'App': 'chats', 'Placeholder_for': 'chat screen', 'chat_id': chat_id, })


def default_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
#    elif request.method == 'POST':
#        return render(request, 'index.html')
    else:
        raise Http405
