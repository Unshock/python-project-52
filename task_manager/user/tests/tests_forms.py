from http import HTTPStatus


from django.urls import reverse
from task_manager.statuses.models import Status
from .settings_for_tests import SettingsUsers
from ..forms import RegisterUserForm, UpdateUserForm, LoginUserForm
from ..models import User
from django.test import Client


class UserFormTest(SettingsUsers):

    def test_valid_register_form(self):
        form = RegisterUserForm(data={
            'username': 'New_user',
            'first_name': 'New_user_first_name',
            'last_name': 'New_user_last_name',
            'password1': 'QWE321rty',
            'password2': 'QWE321rty'
        })

        self.assertTrue(form.is_valid())

    def test_invalid_register_form(self):

        form = RegisterUserForm(data={
            'username': 'New_user'*100,
            'first_name': 'New_user_first_name'*100,
            'last_name': 'New_user_last_name'*100,
            'password1': '1',
            'password2': '1'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_valid_update_form(self):
        form = UpdateUserForm(data={
            'username': 'New_user_updated',
            'first_name': 'New_user_first_name_updated',
            'last_name': 'New_user_last_name_updated',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_update_form(self):

        form = UpdateUserForm(data={
            'username': 'New_user'*100,
            'first_name': 'New_user_first_name'*100,
            'last_name': 'New_user_last_name'*100,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_valid_login_form(self):
        
        print(User.objects.all()[2].is_authenticated)
        print(User.objects.all()[2].username)
        form = LoginUserForm(data={
            'username': 'user_authenticated',
            'password': 'QWE321rty',
        })
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):

        form = LoginUserForm(data={
            'username': 'New_user'*100,
            'password': '1'
        })

        print(form.errors)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
