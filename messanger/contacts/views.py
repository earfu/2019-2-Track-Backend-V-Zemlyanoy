from django.shortcuts import render

from django.http import JsonResponse
from django.http import HttpResponseNotAllowed

# Create your views here.

def index(request):
    if request.method == 'GET':
        return JsonResponse({'App': 'contacts', 'Placeholder_for': 'contact list', })
    else:
        return HttpResponseNotAllowed(['GET'])
