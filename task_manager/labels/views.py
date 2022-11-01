from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label

from django.utils.translation import gettext_lazy as _


class Labels(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'label'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Label list")
        context['label_list'] = Label.objects.all()
        return context


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = LabelForm
    template_name = 'base_create_and_update.html'
    success_url = reverse_lazy('labels')
    success_message = _("Label has been successfully created!")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Create new label")
        context['button_text'] = _("Create")
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = LabelForm
    redirect_field_name = 'redirect_to'
    model = Label
    template_name = "base_create_and_update.html"
    success_url = reverse_lazy('labels')
    success_message = _("Label has been successfully updated!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can update only your labels'))
        return redirect('labels')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update label")
        context['button_text'] = _("Update")

        return context


class DeleteLabel(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Label
    template_name = "base_delete.html"
    success_url = reverse_lazy('labels')
    success_message = _("Label has been successfully deleted!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can delete only your labels'))
        return redirect('labels')

    def post(self, request, *args, **kwargs):

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _(
                'Label that is given to the task can not be deleted'))
            return redirect('labels')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Delete label")
        context['button_text'] = _("Delete")
        context['delete_object'] = str(
            Label.objects.get(id=self.get_object().id))
        return context
