from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label

from django.utils.translation import gettext as _


class Labels(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'label'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Label list")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['label_list'] = Label.objects.all()
        return context

    # сюда довабить фильтр
    def get_queryset(self):
        return Label.objects.all()


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = LabelForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('labels')

    message_text = _("Label has been successfully created!")
    success_message = message_text


    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Label creation")
        action = _("Create new label")
        button_text = _("Create")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['action'] = action
        context['button_text'] = button_text
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = LabelForm
    redirect_field_name = 'redirect_to'
    model = Label
    template_name = "create_user.html"
    success_url = reverse_lazy('labels')

    message_text = _("Label has been successfully updated!")
    success_message = message_text

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can update only your labels')
        messages.error(request, message_text)
        return redirect('labels')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Update label")
        action = _("Update label")
        button_text = _("Update")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text

        return context



class DeleteLabel(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Label
    # username = User.objects.get(id=pk).username надобы написать имя в суксесе
    template_name = "delete_user.html"
    success_url = reverse_lazy('labels')

    message_text = _("Label has been successfully deleted!")
    success_message = message_text

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can delete only your labels')
        messages.error(request, message_text)
        return redirect('labels')

    def post(self, request, *args, **kwargs):

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            message = _('Label that is given to the task can not be deleted')
            messages.error(request, message)
            return redirect('labels')

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Delete label")
        action = _("Delete label")
        button_text = _("Delete")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context
