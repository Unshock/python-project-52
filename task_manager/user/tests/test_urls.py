from http import HTTPStatus
from django.urls import reverse, resolve

from task_manager.user.tests.settings_for_tests import SettingsUsers
from task_manager.user import views


class TestUrls(SettingsUsers):

    def test_users_valid(self):
        url = reverse('users')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Users)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_users_unauthenticated_client(self):
        url = reverse('users')
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Users)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_create_valid(self):
        url = reverse('create_user')
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateUser)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_user.html')

    def test_user_update_valid(self):
        url = reverse('update_user', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateUser)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'update_user.html')

    def test_user_update_unauthenticated_user(self):
        url = reverse('update_user', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateUser)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_update_not_creator_user(self):
        url = reverse('update_user', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateUser)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_delete_valid(self):
        url = reverse('delete_user', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteUser)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_object_template.html')

    def test_user_delete_unauthenticated_user(self):
        url = reverse('delete_user', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteUser)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_delete_not_creator_user(self):
        url = reverse('delete_user', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteUser)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
