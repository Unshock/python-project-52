from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from django.forms import ModelForm

from .models import Status



#from task_manager.user.models import User1



class StatusForm(ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = Status
        #fields = '__all__'
        fields = ['name']