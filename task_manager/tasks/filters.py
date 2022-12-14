import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.forms import FullNameChoiceField
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class FullNameChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = FullNameChoiceField


class TaskFilter(django_filters.FilterSet):
    field_class = FullNameChoiceField

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

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
    labels = django_filters.ModelChoiceFilter(
        label=_("Label"),
        queryset=labels,
        method='filter_by_label',
    )

    executor = FullNameChoiceFilter(
        label=_("Executor"),
        queryset=User.objects.all(),
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
