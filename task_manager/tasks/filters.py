import django_filters
from django import forms
from django.forms import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import MyForm
from task_manager.tasks.models import Task
from task_manager.user.models import User
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy


class TaskFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TaskFilter, self).__init__(*args, **kwargs)

    statuses = Status.objects.all()
    status = django_filters.ModelChoiceFilter(
        label=_("Status"),
        queryset=statuses,
        method='filter_by_status',
    )

    labels = Label.objects.all()
    label = django_filters.ModelChoiceFilter(
        label=gettext_lazy("Label"),
        queryset=labels,
        method='filter_by_label',

    )

    executors = User.objects.all()
    executor = django_filters.ModelChoiceFilter(
        label=gettext_lazy("Executor"),
        queryset=executors,
        method='filter_by_executor',
    )

    self_tasks = django_filters.BooleanFilter(
        label=_("Only my tasks"),
        widget=forms.CheckboxInput(
            attrs={"class": "form-inline"}
        ),
        method='filter_self_tasks'
    )

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=value) if value else queryset

    def filter_by_label(self, queryset, name, value):
        return queryset.filter(labels=value) if value else queryset

    def filter_by_executor(self, queryset, name, value):
        return queryset.filter(executor=value) if value else queryset

    def filter_self_tasks(self, queryset, name, value):
        return queryset.filter(creator=self.user) if value else queryset


