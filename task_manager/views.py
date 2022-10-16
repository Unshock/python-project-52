from django.shortcuts import render
from django.http import HttpResponse
import requests
import os


def index(request, status=None):
    times = int(os.environ.get('TIMES', 3))
    return render(request, 'index.html', context={
        "who": "World"*times,
        "status": status,
    })


def index2(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


def bootdemo(request):
    return render(request, '../DRAFT/bootdemo.html', context={})

