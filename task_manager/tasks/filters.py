import django_filters
from django import forms
from django.forms import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import MyForm
from task_manager.tasks.models import Task
from task_manager.user.models import User


class TaskFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TaskFilter, self).__init__(*args, **kwargs)

    statuses = Status.objects.all()
    status = django_filters.ChoiceFilter(
        label='Status',
        choices=[(status.id, status.name) for status in statuses],
        method='filter_by_status',
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    labels = Label.objects.all()
    label = django_filters.ChoiceFilter(
        label='Label',
        choices=[(label.id, label.name) for label in labels],
        method='filter_by_label',
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
    )

    executors = User.objects.all()
    executor = django_filters.ChoiceFilter(
        label='Executor',
        choices=[(executor.id, executor.username) for executor in executors],
        method='filter_by_executor',
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    self_tasks = django_filters.BooleanFilter(
        label="Only my tasks",
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


