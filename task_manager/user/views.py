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
from django.utils.translation import gettext_lazy as _


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
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return User.objects.all()


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "create_user.html"
    success_url = reverse_lazy('login')
    success_message = _("User has been successfully registered")
    #success_url = redirect('LoginUser', status='U')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create new user")
        context['button_text'] = _("Register user")
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'create_user.html'

    message_text = _("You have been successfully logged in!")
    success_message = message_text

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page_title"] = _("Login")
        context['button_text'] = _("Enter")
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    messages.info(request, _('You have been successfully logged out!'))
    return redirect('home')


class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateUserForm
    model = User
    template_name = "update_user.html"
    success_url = reverse_lazy('users')

    success_message = _("User has been successfully updated!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can\'t update other users')
        messages.error(request, message_text)
        return redirect('users')

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.set_password(request.POST.get('password2'))
        self.object.save()
        return super().post(request, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     form_class = UpdateUserForm(request.POST)
    #     print('formvalid???????????????', form_class.is_valid())
    #     #print(form_class)
    #     print('forminvalid errs', form_class.errors)
    # 
    #     return redirect('users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update user")
        context['button_text'] = _("Update")
        return context

class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = User
    template_name = "delete_object_template.html"
    success_url = reverse_lazy('users')
    success_message = _("User has been successfully deleted!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can\'t delete other users'))
        return redirect('users')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request, _('User that has tasks can not be deleted'))
            return redirect('users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Delete user")
        context['button_text'] = _("Delete")
        context['delete_object'] = self.request.user.get_full_name()
        return context
