from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label=_('Username'), widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    first_name = forms.CharField(
        label=_('First name'), widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    last_name = forms.CharField(
        label=_('Last name'), widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={"class": "form-control"}))


class UpdateUserForm(UserChangeForm):
    password = None

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2
