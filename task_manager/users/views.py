from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.users.forms import RegisterUserForm, LoginUserForm, \
    UpdateUserForm


class UserList(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        return context


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "base_create_and_update.html"
    success_url = reverse_lazy('login')
    success_message = _("User has been successfully registered")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create new users")
        context['button_text'] = _("Register users")
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'base_create_and_update.html'

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
    template_name = "base_create_and_update.html"
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
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            self.object.set_password(request.POST.get('password2'))
            self.object.save()
        return super().post(request, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update users")
        context['button_text'] = _("Update")
        return context


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = User
    template_name = "base_delete.html"
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
        context['page_title'] = _("Delete users")
        context['button_text'] = _("Delete")
        context['delete_object'] = self.request.user.get_full_name()
        return context
