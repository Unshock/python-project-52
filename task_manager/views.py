from django.shortcuts import render
from django.http import HttpResponse
import requests


def index(request):
    return render(request, 'index.html', context={
        "who": "World",
    })


def index2(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

