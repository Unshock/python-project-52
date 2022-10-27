from django.shortcuts import render
from django.http import HttpResponse
import requests
import os


def index(request, status=None):
    # a = None
    # a.hello() # Creating an error with an invalid line of code
    # return HttpResponse("Hello, world. You're at the pollapp index.")
    times = int(os.environ.get('TIMES', 3))
    return render(request, 'base.html', context={
        "who": "World"*times,
        "status": status,
    })


def index2(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


def bootdemo(request):
    return render(request, '../DRAFT/bootdemo.html', context={})

