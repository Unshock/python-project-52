from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class FullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.full_name


class TaskForm(ModelForm):
    name = forms.CharField(
        label=_('Name'), widget=forms.TextInput(
            attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "rows": "10",
                   "cols": "40",
                   })
    )
    executor = FullNameChoiceField(
        label=_('Executor'),
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False,
        empty_label='No executor'
    )
    labels = forms.ModelMultipleChoiceField(
        label=_('Labels'),
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False,
    )
    status = forms.ModelChoiceField(
        label=_('Status'),
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        empty_label='Required field'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'labels', 'status']


class MyForm(forms.Form):
    self_tasks = forms.BooleanField(required=False, initial=False)
