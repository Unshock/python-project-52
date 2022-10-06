from django.shortcuts import render
from django.views import View
from task_manager.user.models import User
from django.http import HttpResponse
# Create your views here.


class Users(View):
    def get(self, request, *args, **kwargs):
        
        user_updated = kwargs.get("user_updated")
        user_created = kwargs.get("user_created")
        
        users = User.objects.all()
        users_list = []
        # print(users_list)
        for user in users:
            user_dict = {}
            user_dict['id'] = user.id
            user_dict['full_name'] = f'{user.first_name} {user.last_name}'
            user_dict['name'] = user.name
            user_dict['timestamp'] = user.timestamp
            users_list.append(user_dict)
        #return render(request, 'index.html', context={"who": [args, kwargs]})
        return render(request, 'users.html', context={"users_objects": users_list,
                                                      "user_updated": user_updated,
                                                      "user_created": user_created})
    
    #def aaa(self):
    #    return self.get(request, )



class CreateUser(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'sign_up.html', context={})

    def post(request):
        # получаем из данных запроса POST отправленные через форму данные
        first_name = request.POST.get("first_name", "Undefined")
        last_name = request.POST.get("last_name", "Undefined")
        name = request.POST.get("name", "Undefined")

        new_user = User()
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.name = name

        new_user.save()

        return Users.get(Users, request, user_created=True)
        return render(request, 'sign_up.html', context={})


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_full_name = User.objects.filter(id=user_id)[0].first_name
        return render(request, 'delete_user.html', context={"user_full_name": user_full_name,
                                                            "user_id": user_id})

    def post(self, request, *args, **kwargs):
        # получаем из данных запроса POST отправленные через форму данные

        user_id = kwargs.get('user_id')
        User.objects.filter(id=user_id).delete()
        return render(request, 'index.html', context={"who": 'f'})


class UpdateUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        return render(request, 'update_user.html', context={"user_id": user_id})

    def post(self, request, *args, **kwargs):

        user_id = kwargs.get('user_id')
        # получаем из данных запроса POST отправленные через форму данные
        first_name = request.POST.get("first_name", "Undefined")
        last_name = request.POST.get("last_name", "Undefined")
        name = request.POST.get("name", "Undefined")

        updating_user = User.objects.filter(id=user_id)[0]
        updating_user.first_name = first_name
        updating_user.last_name = last_name
        updating_user.name = name

        updating_user.save()
        return Users.get(Users, request, user_updated=True)
        #return render(request, "users.html", context={"user_updated": True})


