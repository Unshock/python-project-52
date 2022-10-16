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


def stab(request):
    return redirect('home')


class Statuses(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'status'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Statuses list"
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
    success_message = "Status '%(name)s' was created successfully"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Status creation"
        context['action'] = "Create new status"
        context['button_text'] = "Create"
        #context['creator'] = User.objects.get(id=self.request.user.id)
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
    success_message = "%(name)s has been successfully updated!"
    pk_url_kwarg = "status_id"

    def get(self, request, *args, **kwargs):
        creator_id = Status.objects.get(id=kwargs['status_id']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id == creator_id or user_is_stuff:
            return super().get(request, *args, **kwargs)
        messages.error(request, 'You can update only your statuses')
        return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update status"
        context["action"] = "Update"
        context['button_text'] = "Update"
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
    success_message = "Status has been successfully deleted!"
    pk_url_kwarg = "status_id"

    def get(self, request, *args, **kwargs):

        creator_id = Status.objects.get(id=kwargs['status_id']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff
        if request.user.id == creator_id or user_is_stuff:
            return super().get(request, *args, **kwargs)
        messages.error(request, 'You can delete only your statuses')

        return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete status"
        context["action"] = "Delete status"
        context['button_text'] = "Delete"
        return context
