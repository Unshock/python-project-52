from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm

from .models import User

#from task_manager.user.models import User1



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя', widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    first_name = forms.CharField(
        label='Имя', widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    last_name = forms.CharField(
        label='Фамилия', widget=forms.TextInput(
        attrs={"class": "form-control"}
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))


class UpdateUserForm(UserChangeForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    # password1 = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput(
    #         attrs={"class": "form-control"}
    #     )
    # )
    # password2 = forms.CharField(
    #     label='Повтор пароля',
    #     widget=forms.PasswordInput(
    #         attrs={"class": "form-control"}
    #     )
    # )

    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name']
        #fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class PasswordChangeForm(PasswordChangeForm):

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = User

        #fields = ['username', 'first_name', 'last_name']
        fields = ['password1', 'password2']



