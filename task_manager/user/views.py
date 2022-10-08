from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from task_manager.user.models import User
from django.http import HttpResponse
from task_manager.user.forms import AddUserForm


# Create your views here.


class Users(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Users list"
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return User.objects.all()

    # def get(self, request, *args, **kwargs):
    # 
    #     user_status = kwargs.get("user_status")
    # 
    #     #users = User.objects.all()
    #     # "users_objects": users,
    #     context = {"user_status": user_status,
    #                "title": "Users list",
    #                }
    # 
    #     # users_list = []
    #     # # print(users_list)
    #     # for user in users:
    #     #     user_dict = {}
    #     #     user_dict['id'] = user.id
    #     #     user_dict['full_name'] = f'{user.first_name} {user.last_name}'
    #     #     user_dict['name'] = user.username
    #     #     user_dict['timestamp'] = user.timestamp
    #     #     users_list.append(user_dict)
    #     #return render(request, 'index.html', context={"who": [args, kwargs]})
    #     
    #     return render(request, 'users/users.html', context=context)
    
    #def aaa(self):
    #    return self.get(request, )


class CreateUser3(CreateView):
    form_class = AddUserForm
    template_name = "create_user.html"
    success_url = reverse_lazy('users')#, user_status="created")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Users list"
        context["action"] = "Create new user"
        context['button_text'] = "Create"
        #context['user_status'] = "Created"
        return context

    # def get(self, request, *args, **kwargs):
    #     form_class = AddUserForm()
    #     context = {"form": form_class,
    #                "action": "Create new user",
    #                "button_text": "Create"}
    # 
    #     return render(request, 'create_user.html', context=context)
    # 
    # def post(self, request, *args, **kwargs):
    #     # получаем из данных запроса POST отправленные через форму данные
    #     form = AddUserForm(request.POST)
    # 
    #     if form.is_valid():
    #         form.save()
    #         return Users.get(Users, request, user_status="created")
            #return redirect('users')

        #return Users.get(Users, request, user_status="created")
        #return render(request, 'create_user.html', context={})


class UpdateUser(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = "update_user.html"
    success_url = reverse_lazy('users')#, user_status="created")
    pk_url_kwarg = "user_id"


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update user"
        context["action"] = "Update"
        context['button_text'] = "Update"

        #context['user_status'] = "Created"
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["first_name"].widget.attrs["class"] = "form-control"
        form.fields["last_name"].widget.attrs["class"] = "form-control"
        form.fields["username"].widget.attrs["class"] = "form-control"
        return form

class UpdateUser_no(View):
    def get(self, request, *args, **kwargs):
        form = AddUserForm()
        context = {"form": form,
                   "action": "Update user",
                   "button_text": "Update"}

        return render(request, 'create_user.html', context=context)


    def post(self, request, *args, **kwargs):
        form = AddUserForm(request.POST)

        if form.is_valid():
            form.save()
            return Users.get(Users, request, user_status="updated")

class CreateUser(View):

    def get(self, request, *args, **kwargs):

        text_params = [
            {'name': 'first_name', 'text': "First name"},
            {'name': 'last_name', 'text': "Last name"},
            {'name': 'username', 'text': "Nickname"},
        ]

        context = {"text_params": text_params,
                   "form_action": '/users/create/',
                   "action": "Create"}

        return render(request, '../../DRAFT/base_user_CU.html', context=context)

    def post(self, request, *args, **kwargs):
        # получаем из данных запроса POST отправленные через форму данные
        first_name = request.POST.get("first_name", "Undefined")
        last_name = request.POST.get("last_name", "Undefined")
        name = request.POST.get("username", "Undefined")

        new_user = User()
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.username = name

        new_user.save()

        return Users.get(Users, request, user_status="created")
        #return render(request, 'create_user.html', context={})


class DeleteUser(DeleteView):
    model = User
    template_name = "delete_user.html"
    success_url = reverse_lazy('users')#, user_status="created")
    pk_url_kwarg = "user_id"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete user"
        context["action"] = "Create new user"
        context['button_text'] = "Delete"
        #context['user_status'] = "Deleted"
        return context

class DeleteUser2(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)

        context = {"user_full_name": user.full_name}

        return render(request, 'delete_user.html', context=context)

    def post(self, request, *args, **kwargs):
        # получаем из данных запроса POST отправленные через форму данные

        user_id = kwargs.get('user_id')
        User.objects.filter(id=user_id).delete()
        return Users.get(Users, request, user_status="deleted")


class UpdateUser2(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        text_params = [
            {'name': 'first_name', 'text': "First name"},
            {'name': 'last_name', 'text': "Last name"},
            {'name': 'username', 'text': "Nickname"},
        ]

        context = {"form_action": f'/users/{user_id}/update/',
                   "action": "Update",
                   "text_params": text_params}

        return render(request, '../../DRAFT/base_user_CU.html', context=context)

    def post(self, request, *args, **kwargs):

        user_id = kwargs.get('user_id')
        # получаем из данных запроса POST отправленные через форму данные
        first_name = request.POST.get("first_name", "Undefined")
        last_name = request.POST.get("last_name", "Undefined")
        name = request.POST.get("username", "Undefined")

        updating_user = User.objects.get(id=user_id)
        updating_user.first_name = first_name
        updating_user.last_name = last_name
        updating_user.username = name

        updating_user.save()
        return Users.get(Users, request, user_status="updated")
        #return render(request, "users.html", context={"user_updated": True})


