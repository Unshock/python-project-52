from django.shortcuts import render
from django.views import View
from task_manager.user.models import User
from django.http import HttpResponse
# Create your views here.


class CreateUser(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'user_creation.html', context={})

    def post(request):
        # получаем из данных запроса POST отправленные через форму данные
        name = request.POST.get("name", "Undefined")

        new_user = User()
        new_user.name = name
        new_user.save()

        return render(request, 'user_creation.html', context={})


