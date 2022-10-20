from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from task_manager.statuses.models import Status
from task_manager.tasks.forms import CreateTaskForm, UpdateTaskForm
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _

from task_manager.user.models import User


class Tasks(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Task list")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['task_list'] = Task.objects.all()
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Status.objects.all()


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    message_text = _("Task has been successfully created!")
    success_message = message_text


    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Task creation")
        action = _("Create new task")
        button_text = _("Create")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['action'] = action
        context['button_text'] = button_text
        #print(context)
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateTaskForm
    redirect_field_name = 'redirect_to'
    model = Task
    #fields = ['name', 'description', 'status', 'executor']
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy('tasks')

    message_text = _("Task has been successfully updated!")
    success_message = message_text

    def get(self, request, *args, **kwargs):
        creator_id = Task.objects.get(id=kwargs['pk']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff

        if request.user.id != creator_id and not user_is_stuff:
            message_text = _('You can update only your tasks')
            messages.error(request, message_text)
            return redirect('tasks')
        
        preselected = Task.objects.get(id=kwargs['pk']).labels
        #print(Task.objects.get(id=kwargs['pk']).labels.all())
        #print('1111111111111111111', preselected, kwargs['pk'])
        print(super().get(request, *args, **kwargs))
        return super().get(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Update task")
        action = _("Update task")
        button_text = _("Update")
        context = super().get_context_data(**kwargs)
        #context['initial'] = Task.objects.get(id=kwargs['pk']).all()
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context

    def get_initial(self):
        initial = super().get_initial()
        task = Task.objects.get(id=self.kwargs['pk'])

        initial['labels'] = task.labels.all()
        return initial


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Task
    # username = User.objects.get(id=pk).username надобы написать имя в суксесе
    template_name = "delete_user.html"
    success_url = reverse_lazy('tasks')

    message_text = _("Task has been successfully deleted!")
    success_message = message_text


    def get(self, request, *args, **kwargs):
        creator_id = Task.objects.get(id=kwargs['pk']).creator_id
        user_is_stuff = User.objects.get(id=request.user.id).is_staff

        if request.user.id != creator_id and not user_is_stuff:
            message_text = _('You can delete only your tasks')
            messages.error(request, message_text)
            return redirect('tasks')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Delete task")
        action = _("Delete task")
        button_text = _("Delete")

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context["action"] = action
        context['button_text'] = button_text
        return context


class DetailTask(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = _("Detailed task")
        context = super().get_context_data(**kwargs)
        context['title'] = title
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Task.objects.all()
