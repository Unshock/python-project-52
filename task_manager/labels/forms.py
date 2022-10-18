from django.forms import ModelForm
from django import forms

from task_manager.labels.models import Label


class CreateLabelForm(ModelForm):
    name = forms.CharField(
        label='Имя', widget=forms.TextInput(
            attrs={"class": "form-control"})
    )

    class Meta:
        model = Label
        fields = ['name']


class UpdateLabelForm(ModelForm):
    name = forms.CharField(
        label='Имя', widget=forms.TextInput(
            attrs={"class": "form-control"})
    )

    class Meta:
        model = Label
        fields = ['name']