from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __


class Statuses(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'status'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Status list")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['status_list'] = Status.objects.all()
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Status.objects.all()


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = StatusForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('statuses')

    message_text = __("Status has been successfully created!")
    success_message = message_text

    def get_context_data(self, *, object_list=None, **kwargs):
        title = __("Status creation")
        action = __("Create new status")
        button_text = __("Create")

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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can update only your statuses')
        messages.error(request, message_text)
        return redirect('statuses')

    # def get(self, request, *args, **kwargs):
    #     creator_id = Status.objects.get(id=kwargs['pk']).creator_id
    #     user_is_stuff = User.objects.get(id=request.user.id).is_staff
    #     if request.user.id == creator_id or user_is_stuff:
    #         return super().get(request, *args, **kwargs)
    # 
    #     message_text = _('You can update only your statuses')
    #     messages.error(request, message_text)
    #     return redirect('statuses')

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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        message_text = _('You can update only your labels')
        messages.error(request, message_text)
        return redirect('labels')
    # 
    # def get(self, request, *args, **kwargs):
    # 
    #     creator_id = Status.objects.get(id=kwargs['pk']).creator_id
    #     user_is_stuff = User.objects.get(id=request.user.id).is_staff
    #     if request.user.id == creator_id or user_is_stuff:
    #         return super().get(request, *args, **kwargs)
    # 
    #     message_text = _('You can delete only your statuses')
    #     messages.error(request, message_text)
    # 
    #     return redirect('statuses')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            message = _('Status that is used for tasks can not be deleted')
            messages.error(request, message)
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
