from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.user.models import User
from django.utils.translation import gettext as _


class Statuses(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'status'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Status list")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['statuses_list'] = Status.objects.all()
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Status.objects.all()


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = CreateStatusForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('statuses')

    message_text = _("Status has been successfully created!")
    success_message = message_text


    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Status creation")
        action = _("Create new status")
        button_text = _("Create")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['action'] = action
        context['button_text'] = button_text
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Status
    fields = ['name']
    template_name = "update_user.html"
    success_url = reverse_lazy('statuses')

    message_text = _("Status has been successfully updated!")
    success_message = message_text

    pk_url_kwarg = "status_id"

    def get(self, request, *args, **kwargs):
        creator_id = Status.objects.get(id=kwargs['status_id']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id == creator_id or user_is_stuff:
            return super().get(request, *args, **kwargs)

        message_text = _('You can update only your statuses')
        messages.error(request, message_text)
        return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Update status")
        action = _("Update status")
        button_text = _("Update")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Status
    #username = User.objects.get(id=pk).username надобы написать имя в суксесе
    template_name = "delete_user.html"
    success_url = reverse_lazy('statuses')

    message_text = _("Status has been successfully deleted!")
    success_message = message_text
    pk_url_kwarg = "status_id"

    def get(self, request, *args, **kwargs):

        creator_id = Status.objects.get(id=kwargs['status_id']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id == creator_id or user_is_stuff:
            return super().get(request, *args, **kwargs)

        message_text = _('You can delete only your statuses')
        messages.error(request, message_text)

        return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Delete status")
        action = _("Delete status")
        button_text = _("Delete")
        
        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context
