from django import forms
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
#from django.contrib.auth.models import User
from .models import User
from task_manager.views import index
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy


#from task_manager.user.models import User1
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.user.forms import RegisterUserForm, LoginUserForm, \
    UpdateUserForm

from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


class Users(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("User list")
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        context['title'] = title
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return User.objects.all()


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "create_user.html"
    success_url = reverse_lazy('login')
    success_message = gettext_lazy("User has been successfully registered")
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

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('home')


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'create_user.html'

    message_text = gettext_lazy("You have been successfully logged in!")
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
    form_class = UpdateUserForm
    model = User
    template_name = "update_user.html"
    success_url = reverse_lazy('users')

    message_text = _("has been successfully updated!")
    success_message = "%(username)s " + message_text

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can\'t update other users')
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


class ChangePassword(LoginRequiredMixin,
                     SuccessMessageMixin,
                     PasswordChangeView):
    login_url = 'login'
    model = User
    template_name = "update_user.html"
    success_url = reverse_lazy('users')

    success_message = _("Password has been successfully changed!")

    def get_context_data(self, *, object_list=None, **kwargs):

        title = _("Change password")
        action = _("Change password")
        button_text = _("Change")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text

        return context


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = User
    template_name = "delete_user.html"
    success_url = reverse_lazy('users')

    message_text = _("User has been successfully deleted!")
    success_message = message_text

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can\'t delete other users')
        messages.error(request, message_text)
        return redirect('users')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            message = _('User that has tasks can not be deleted')
            messages.error(request, message)
            return redirect('users')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Delete user")
        action = _("Delete user")
        button_text = _("Delete")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context
