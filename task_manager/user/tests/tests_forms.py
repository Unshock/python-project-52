from http import HTTPStatus
from django.urls import reverse
from task_manager.statuses.models import Status
from .tests_settings import SettingsUsers
from ..models import User
from django.test import Client


class UserFormTest(SettingsUsers):
    def test_valid_creation_form(self):

        user_count_before = User.objects.count()

        form_data = {
            'username': 'New_user',
            'first_name': 'John',
            'last_name': 'Novichek',
            'password1': 'qweR19Tyui',
            'password2': 'qweR19Tyui'
        }

        response = self.client.post(
            reverse('create_user'),
            data=form_data,
            follow=True
        )

        user_count_after = User.objects.count()
        created_object = User.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user_count_before + 1, user_count_after)
        self.assertEqual(user_count_after, 3)
        self.assertEqual(created_object.id, 3)
        self.assertEqual(created_object.username, "New_user")
        self.assertEqual(created_object.first_name, "John")
        self.assertEqual(created_object.last_name, "Novichek")
        self.assertTrue(created_object.password)



    def test_invalid_creation_form(self):

        user_count_before = User.objects.count()

        invalid_form_data = {
            'username': 'New_user',
            'first_name': 'John',
            'last_name': 'Novichek',
            'password1': '1',
            'password2': '1'
        }

        response = self.client.post(
            reverse('create_user'),
            data=invalid_form_data,
            follow=True
        )

        user_count_after = User.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(user_count_after, 2)


    def test_valid_update_form(self):

        user_count_before = User.objects.count()

        create_form_data = {
            'username': 'New_user',
            'first_name': 'John',
            'last_name': 'Novichek',
            'password1': 'qweR19Tyui',
            'password2': 'qweR19Tyui'
        }

        client_new = Client()
        create_response = self.client.post(
            reverse('create_user'),
            data=create_form_data,
            follow=True
        )

        user_new = User.objects.last()
        client_new.force_login(user_new)

        created_object = User.objects.last()

        update_form_data = {
            'username': 'New_user-update',
            'first_name': 'John-update',
            'last_name': 'Novichek-update',
            'password1': 'qweR19Tyui',
            'password2': 'qweR19Tyui'
        }

        response = client_new.post(
            reverse('update_user', kwargs={'user_id': created_object.pk}),
            data=update_form_data,
            follow=True
        )

        user_count_after = User.objects.count()
        updated_object = User.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(user_count_before + 1, user_count_after)
        self.assertEqual(user_count_after, 3)
        self.assertEqual(updated_object.id, 3)
        self.assertEqual(updated_object.username, "New_user-update")
        self.assertEqual(updated_object.first_name, "John-update")
        self.assertEqual(updated_object.last_name, "Novichek-update")
        self.assertTrue(updated_object.password)


    def test_invalid_update_form(self):

        user_count_before = User.objects.count()

        create_form_data = {
            'username': 'New_user',
            'first_name': 'John',
            'last_name': 'Novichek',
            'password1': 'qweR19Tyui',
            'password2': 'qweR19Tyui'
        }

        client_new = Client()
        create_response = self.client.post(
            reverse('create_user'),
            data=create_form_data,
            follow=True
        )

        user_new = User.objects.last()
        client_new.force_login(user_new)

        created_object = User.objects.last()

        update_form_data = {
            'username': 'New_user-update'*100,
            'first_name': 'John-update',
            'last_name': 'Novichek-update',
        }

        response = client_new.post(
            reverse('update_user', kwargs={'user_id': created_object.pk}),
            data=update_form_data,
            follow=True
        )

        user_count_after = User.objects.count()
        updated_object = User.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_count_before + 1, user_count_after)
        self.assertEqual(user_count_after, 3)
        self.assertEqual(updated_object.id, 3)
        self.assertEqual(updated_object.username, "New_user")
        self.assertEqual(updated_object.first_name, "John")
        self.assertEqual(updated_object.last_name, "Novichek")
        self.assertTrue(updated_object.password)
