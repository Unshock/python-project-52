from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusForm(ModelForm):
    name = forms.CharField(label=_("Name"), widget=forms.TextInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = Status
        fields = ['name']
