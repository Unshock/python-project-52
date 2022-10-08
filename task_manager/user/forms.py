from django import forms
from task_manager.user.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
        }


