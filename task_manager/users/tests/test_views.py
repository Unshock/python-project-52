from http import HTTPStatus
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .settings_for_tests import SettingsUsers
from ..models import User


class TestUsersViews(SettingsUsers):

    def setUp(self):
        self.list_url = reverse('users')
        self.create_url = reverse('create_user')
        self.update_url = reverse('update_user', kwargs={'pk': 1})
        self.delete_url = reverse('delete_user', kwargs={'pk': 1})
        self.login_url = reverse('login')

    def test_user_list_GET(self):

        response = self.client_authenticated.get(self.list_url)
        user_list = response.context.get('user_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(user_list), 3)
        self.assertEqual(user_list[0].username, 'user_authenticated')
        self.assertEqual(user_list[2].username, 'user_unauthenticated')
        self.assertEqual(user_list[1].first_name, 'AuthenticatedNotCreator')
        self.assertEqual(user_list[1].last_name, 'UserNotAdmin')
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_list_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.list_url)
        user_list = response.context.get('user_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(user_list), 3)
        self.assertEqual(user_list[0].username, 'user_authenticated')
        self.assertEqual(user_list[2].username, 'user_unauthenticated')
        self.assertEqual(user_list[1].first_name, 'AuthenticatedNotCreator')
        self.assertEqual(user_list[1].last_name, 'UserNotAdmin')
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_create_user_GET(self):
        response = self.client_authenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context.get('page_title'), _('Create new users'))
        self.assertEqual(
            response.context.get('button_text'), _('Register users'))
        self.assertTemplateUsed(response, 'base_create_and_update.html')

    def test_create_user_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context.get('page_title'), _('Create new users'))
        self.assertEqual(
            response.context.get('button_text'), _('Register users'))
        self.assertTemplateUsed(response, 'base_create_and_update.html')

    def test_create_task_POST(self):
        self.assertEqual(User.objects.all().count(), 3)

        user_data = {
            'username': 'Test_user',
            'first_name': 'Test_user_first_name',
            'last_name': 'Test_user_last_name',
            'password1': 'TestPassword987654',
            'password2': 'TestPassword987654'
        }

        response = self.client_unauthenticated.post(
            self.create_url, user_data)

        created_user = User.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 4)
        self.assertEqual(created_user.username, 'Test_user')
        self.assertEqual(created_user.first_name, 'Test_user_first_name')
        self.assertEqual(created_user.last_name, 'Test_user_last_name')
        self.assertTrue(created_user.password)
        self.assertEqual(created_user.id, 4)
        self.assertRedirects(response, self.login_url)

    def test_update_user_GET(self):
        response = self.client_authenticated.get(self.update_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Update users'))
        self.assertEqual(response.context.get('button_text'), _('Update'))
        self.assertTemplateUsed(response, 'base_create_and_update.html')

    def test_update_user_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_user_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_user_POST(self):
        self.assertEqual(User.objects.all().count(), 3)

        user_data = {
            'username': 'Updated_user',
            'first_name': 'Updated_user_first_name_',
            'last_name': 'Updated_user_last_name',
            'password1': '111',
            'password2': '111'
        }

        response = self.client_authenticated.post(
            self.update_url, user_data)

        updated_user = User.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(updated_user.username, 'Updated_user')
        self.assertEqual(updated_user.first_name, 'Updated_user_first_name_')
        self.assertEqual(updated_user.last_name, 'Updated_user_last_name')
        self.assertEqual(updated_user.id, 1)
        self.assertRedirects(response, self.list_url)

    def test_update_user_POST_unauthenticated_client(self):
        self.assertEqual(User.objects.all().count(), 3)

        user_data = {
            'username': 'Updated_user',
            'first_name': 'Updated_user_first_name_',
            'last_name': 'Updated_user_last_name',
        }

        response = self.client_unauthenticated.post(
            self.update_url, user_data)

        updated_user = User.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(updated_user.username, 'user_authenticated')
        self.assertEqual(updated_user.first_name, 'Authenticated')
        self.assertEqual(updated_user.last_name, 'UserNotAdmin')
        self.assertEqual(updated_user.id, 1)

    def test_update_user_POST_client_not_creator(self):
        self.assertEqual(User.objects.all().count(), 3)

        user_data = {
            'username': 'Updated_user',
            'first_name': 'Updated_user_first_name_',
            'last_name': 'Updated_user_last_name',
        }

        response = self.client_unauthenticated.post(
            self.update_url, user_data)

        updated_user = User.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(updated_user.username, 'user_authenticated')
        self.assertEqual(updated_user.first_name, 'Authenticated')
        self.assertEqual(updated_user.last_name, 'UserNotAdmin')
        self.assertEqual(updated_user.id, 1)

    def test_delete_user_GET(self):
        response = self.client_authenticated.get(self.delete_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Delete users'))
        self.assertEqual(response.context.get('button_text'), _('Delete'))
        self.assertTemplateUsed(response, 'base_delete.html')

    def test_delete_user_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_user_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_user_POST(self):
        self.assertEqual(User.objects.all().count(), 3)

        response = self.client_authenticated.post(
            self.delete_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(User.objects.first().username,
                         'user_authenticated_not_creator')
        self.assertRedirects(response, self.list_url)

    def test_delete_user_POST_user_is_task_executor(self):
        self.assertEqual(User.objects.all().count(), 3)

        response = self.client_authenticated.post(
            reverse('delete_user', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertRedirects(response, self.list_url)

    def test_delete_user_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.first().username, 'user_authenticated')

    def test_delete_user_POST_client_not_creator(self):
        response = self.client_authenticated_not_creator.post(
            self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.first().username, 'user_authenticated')
