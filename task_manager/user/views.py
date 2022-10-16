from django import forms
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.utils.translation import gettext as _


#from task_manager.user.models import User1
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.user.forms import RegisterUserForm, LoginUserForm


# Create your views here.


class Users(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Users list")
        context = super().get_context_data(**kwargs)
        context['users_list'] = User.objects.all()
        context['title'] = title
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return User.objects.all()


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "create_user.html"
    success_url = reverse_lazy('login')
    success_message = "%(username)s was created successfully"
    #success_url = redirect('LoginUser', status='U')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("User creation")
        action = _("Create new user")
        button_text = _("Create")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context
    
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('home')
    
    
class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'create_user.html'

    message_text = _("You have been successfully logged in!")
    success_message = message_text

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Login")
        action = _("Login")
        button_text = _("Login")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    message_text = _('You have been successfully logged out!')
    messages.info(request, message_text)
    return redirect('home')


class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = "update_user.html"
    success_url = reverse_lazy('users')

    message_text = _("has been successfully updated!")
    success_message = "%(username)s " + message_text
    pk_url_kwarg = "user_id"


    def get(self, request, *args, **kwargs):
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id == kwargs['user_id'] or user_is_stuff:
            return super().get(request, *args, **kwargs)

        message_text = _('You do not have permission to update another user')
        messages.error(request, message_text)
        return redirect('users')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Update user")
        action = _("Update user")
        button_text = _("Update")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text

        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["first_name"].widget.attrs["class"] = "form-control"
        form.fields["last_name"].widget.attrs["class"] = "form-control"
        form.fields["username"].widget.attrs["class"] = "form-control"
        #form.fields["password1"].widget.attrs["class"] = "form-control"
        #form.fields["password2"].widget.attrs["class"] = "form-control"
        return form


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = User
    #username = User.objects.get(id=pk).username надобы написать имя в суксесе
    template_name = "delete_user.html"
    success_url = reverse_lazy('users')

    message_text = _("User has been successfully deleted!")
    success_message = message_text
    pk_url_kwarg = "user_id"

    def get(self, request, *args, **kwargs):
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id != kwargs['user_id'] and not user_is_stuff:
            message = _('You do not have permission to delete another user')
            messages.error(request, message)
            return redirect('users')

        if len(User.objects.get(id=kwargs['user_id']).executor.all()) > 0:
            message = _('User that has tasks can not be deleted')
            messages.error(request, message)
            return redirect('users')

        return super().get(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Delete user")
        action = _("Delete user")
        button_text = _("Delete")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context
