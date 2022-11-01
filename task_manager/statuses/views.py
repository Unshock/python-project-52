from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


class Statuses(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'status'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Status list")
        context['status_list'] = Status.objects.all()
        return context


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = StatusForm
    template_name = 'base_create_and_update.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Status has been successfully created!")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Create new status")
        context['button_text'] = _("Create")
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Status
    fields = ['name']
    template_name = "base_create_and_update.html"
    success_url = reverse_lazy('statuses')

    success_message = _("Status has been successfully updated!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can update only your statuses'))
        return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update status")
        context['button_text'] = _("Update")
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Status
    template_name = "base_delete.html"
    success_url = reverse_lazy('statuses')

    message_text = _("Status has been successfully deleted!")
    success_message = message_text

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can update only your labels')
        messages.error(request, message_text)
        return redirect('labels')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _(
                'Status that is used for tasks can not be deleted'))
            return redirect('statuses')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Delete status")
        context['button_text'] = _("Delete")
        context['delete_object'] = str(
            Status.objects.get(id=self.get_object().id))
        return context
