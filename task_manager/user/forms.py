from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.forms import ModelForm

from .models import User
from django.utils.translation import gettext_lazy
#from task_manager.user.models import User1



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label=gettext_lazy('Username'), widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    first_name = forms.CharField(
        label=gettext_lazy('First name'), widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    last_name = forms.CharField(
        label=gettext_lazy('Last name'), widget=forms.TextInput(
        attrs={"class": "form-control"}
        )
    )
    password1 = forms.CharField(
        label=gettext_lazy('Password'),
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label=gettext_lazy('Password confirmation'),
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=gettext_lazy("Username"), widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label=gettext_lazy('Password'), widget=forms.PasswordInput(
        attrs={"class": "form-control"}))


class UpdateUserForm(UserChangeForm):
    password = None

    username = forms.CharField(
        label=gettext_lazy('Username'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label=gettext_lazy('First name'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label=gettext_lazy('Last name'),
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label=gettext_lazy('Password'),
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label=gettext_lazy('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(gettext_lazy("Passwords don't match"))
        return password2
#     
#     
# class UpdateUserForm(UserChangeForm):
# 
#     username = forms.CharField(
#         label=gettext_lazy('Username'),
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     first_name = forms.CharField(
#         label=gettext_lazy('First name'),
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     last_name = forms.CharField(
#         label=gettext_lazy('Last name'),
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
# 
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name']
#         #fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
# 

# class PasswordChangeForm(PasswordChangeForm):
# 
#     password1 = forms.CharField(
#         label=gettext_lazy('Password'),
#         widget=forms.PasswordInput(
#             attrs={"class": "form-control"}
#         )
#     )
#     password2 = forms.CharField(
#         label=gettext_lazy('Password confirmation'),
#         widget=forms.PasswordInput(
#             attrs={"class": "form-control"}
#         )
#     )
# 
#     class Meta:
#         model = User
# 
#         #fields = ['username', 'first_name', 'last_name']
#         fields = ['password1', 'password2']



