from django import forms
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
#from django.contrib.auth.models import User
from .models import User
from task_manager.views import index

#from task_manager.user.models import User1
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.user.forms import RegisterUserForm, LoginUserForm


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
    #     #     user_dict['creation_date'] = user.creation_date
    #     #     users_list.append(user_dict)
    #     #return render(request, 'index.html', context={"who": [args, kwargs]})
    #     
    #     return render(request, 'users/users.html', context=context)
    
    #def aaa(self):
    #    return self.get(request, )


class CreateUser3(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "create_user.html"
    success_url = reverse_lazy('login')
    success_message = "%(username)s was created successfully"
    #success_url = redirect('LoginUser', status='U')


    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Users list"
        context["action"] = "Create new user"
        context['button_text'] = "Create"
        #context['user_status'] = "Created"
        return context
    
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('home')
    
    
class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'create_user.html'
    success_message = "You have been successfully logged in!"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        context["action"] = "Login"
        context['button_text'] = "Login"
        #context['user_status'] = "Created"
        return context
    
    def get_success_url(self):
        
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    messages.info(request, 'You have successfully logged out!')
    return redirect('home')
# 
#     # def get(self, request, *args, **kwargs):
#     #     form_class = AddUserForm()
#     #     context = {"form": form_class,
#     #                "action": "Create new user",
#     #                "button_text": "Create"}
#     # 
#     #     return render(request, 'create_user.html', context=context)
#     # 
#     # def post(self, request, *args, **kwargs):
#     #     # получаем из данных запроса POST отправленные через форму данные
#     #     form = AddUserForm(request.POST)
#     # 
#     #     if form.is_valid():
#     #         form.save()
#     #         return Users.get(Users, request, user_status="created")
#             #return redirect('users')
# 
#         #return Users.get(Users, request, user_status="created")
#         #return render(request, 'create_user.html', context={})
# 
# 

class UpdateUser(SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = "update_user.html"
    success_url = reverse_lazy('users')
    success_message = "%(username)s has been successfully updated!"
    pk_url_kwarg = "user_id"
    print(pk_url_kwarg)

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['user_id']:
            messages.error(request, 'You do not have permission to update another user')
            return redirect('users')
        return super().get(request, *args, **kwargs)

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
        #form.fields["password1"].widget.attrs["class"] = "form-control"
        #form.fields["password2"].widget.attrs["class"] = "form-control"
        return form


# 
# class UpdateUser_no(View):
#     def get(self, request, *args, **kwargs):
#         form = RegisterUserForm()
#         context = {"form": form,
#                    "action": "Update user",
#                    "button_text": "Update"}
# 
#         return render(request, 'create_user.html', context=context)
# 
# 
#     def post(self, request, *args, **kwargs):
#         form = AddUserForm(request.POST)
# 
#         if form.is_valid():
#             form.save()
#             return Users.get(Users, request, user_status="updated")
# 
# class CreateUser(View):
# 
#     def get(self, request, *args, **kwargs):
# 
#         text_params = [
#             {'name': 'first_name', 'text': "First name"},
#             {'name': 'last_name', 'text': "Last name"},
#             {'name': 'username', 'text': "Nickname"},
#         ]
# 
#         context = {"text_params": text_params,
#                    "form_action": '/users/create/',
#                    "action": "Create"}
# 
#         return render(request, '../../DRAFT/base_user_CU.html', context=context)
# 
#     def post(self, request, *args, **kwargs):
#         # получаем из данных запроса POST отправленные через форму данные
#         first_name = request.POST.get("first_name", "Undefined")
#         last_name = request.POST.get("last_name", "Undefined")
#         name = request.POST.get("username", "Undefined")
# 
#         new_user = User1()
#         new_user.first_name = first_name
#         new_user.last_name = last_name
#         new_user.username = name
# 
#         new_user.save()
# 
#         return Users.get(Users, request, user_status="created")
#         #return render(request, 'create_user.html', context={})
# 
# 
class DeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    #username = User.objects.get(id=pk).username надобы написать имя в суксесе
    template_name = "delete_user.html"
    success_url = reverse_lazy('users')
    success_message = "User has been successfully deleted!"
    pk_url_kwarg = "user_id"

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['user_id']:
            messages.error(request, 'You do not have permission to update another user')
            return redirect('users')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete user"
        context["action"] = "Delete user"
        context['button_text'] = "Delete"
        #context['user_status'] = "Deleted"
        return context
# 
# class DeleteUser2(View):
#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get('user_id')
#         user = User1.objects.get(id=user_id)
# 
#         context = {"user_full_name": user.full_name}
# 
#         return render(request, 'delete_user.html', context=context)
# 
#     def post(self, request, *args, **kwargs):
#         # получаем из данных запроса POST отправленные через форму данные
# 
#         user_id = kwargs.get('user_id')
#         User1.objects.filter(id=user_id).delete()
#         return Users.get(Users, request, user_status="deleted")
# 
# 
# class UpdateUser2(View):
#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get('user_id')
# 
#         text_params = [
#             {'name': 'first_name', 'text': "First name"},
#             {'name': 'last_name', 'text': "Last name"},
#             {'name': 'username', 'text': "Nickname"},
#         ]
# 
#         context = {"form_action": f'/users/{user_id}/update/',
#                    "action": "Update",
#                    "text_params": text_params}
# 
#         return render(request, '../../DRAFT/base_user_CU.html', context=context)
# 
#     def post(self, request, *args, **kwargs):
# 
#         user_id = kwargs.get('user_id')
#         # получаем из данных запроса POST отправленные через форму данные
#         first_name = request.POST.get("first_name", "Undefined")
#         last_name = request.POST.get("last_name", "Undefined")
#         name = request.POST.get("username", "Undefined")
# 
#         updating_user = User1.objects.get(id=user_id)
#         updating_user.first_name = first_name
#         updating_user.last_name = last_name
#         updating_user.username = name
# 
#         updating_user.save()
#         return Users.get(Users, request, user_status="updated")
#         #return render(request, "users.html", context={"user_updated": True})


