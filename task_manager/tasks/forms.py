from django.forms import ModelForm
from django import forms

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.user.models import User


class TaskForm(ModelForm):
    name = forms.CharField(
        label='Имя', widget=forms.TextInput(
            attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "rows": "10",
                   "cols": "40",
                   })
    )
    executor = forms.ModelChoiceField(
        label='Исполнитель',
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False,
        empty_label='No executor'
    )
    labels = forms.ModelMultipleChoiceField(
        label='Метки',
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False,
    )
    status = forms.ModelChoiceField(
        label='Статус',
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
            ),
        empty_label='Required field'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'labels', 'status']
