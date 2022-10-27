from http import HTTPStatus
from django.urls import reverse, resolve
from task_manager.statuses import views
from task_manager.statuses.tests.settings_for_tests import SettingsStatuses


class TestUrls(SettingsStatuses):

    def test_statuses_valid(self):
        url = reverse('statuses')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Statuses)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/status_list.html')


    def test_statuses_unauthenticated_client(self):
        url = reverse('statuses')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Statuses)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_status_create_valid(self):
        url = reverse('create_status')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateStatus)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_user.html')


    def test_status_create_unauthenticated_user(self):
        url = reverse('create_status')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateStatus)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_status_update_valid(self):
        url = reverse('update_status', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateStatus)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'update_user.html')


    def test_status_update_unauthenticated_user(self):
        url = reverse('update_status', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateStatus)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_status_update_not_creator_user(self):
        url = reverse('update_status', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateStatus)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_status_delete_valid(self):
        url = reverse('delete_status', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteStatus)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_object_template.html')


    def test_status_delete_unauthenticated_user(self):
        url = reverse('delete_status', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteStatus)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_status_delete_not_creator_user(self):
        url = reverse('delete_status', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteStatus)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
