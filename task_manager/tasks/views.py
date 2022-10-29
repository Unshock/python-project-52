from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,\
    DeleteView, DetailView

from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.tasks import filters
from task_manager.user.models import User


class Tasks(LoginRequiredMixin, ListView):
    queryset = Task.objects.all()
    login_url = 'login'
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = filters.TaskFilter(
            self.request.GET,
            queryset=queryset,
            user=self.request.user.id
        )
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        context['page_title'] = _("Task list")
        return context


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    message_text = _("Task has been successfully created!")
    success_message = message_text

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Create new task")
        context['button_text'] = _("Create")
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = TaskForm
    redirect_field_name = 'redirect_to'
    model = Task
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy('tasks')
    success_message = _("Task has been successfully updated!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can update only your tasks'))
        return redirect('tasks')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update task")
        context['button_text'] = _("Update")
        return context

    def get_initial(self):
        initial = super().get_initial()
        task = Task.objects.get(id=self.kwargs['pk'])
        initial['labels'] = task.labels.all()
        return initial


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Task
    template_name = "delete_object_template.html"
    success_url = reverse_lazy('tasks')

    success_message = _("Task has been successfully deleted!")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator.id == request.user.id \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, _('You can delete only your tasks'))
        return redirect('tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Delete task")
        context['button_text'] = _("Delete")
        context['delete_object'] = str(
            Task.objects.get(id=self.get_object().id))
        return context


class DetailTask(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Detailed task")
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Task.objects.all()
