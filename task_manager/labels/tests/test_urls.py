from http import HTTPStatus
from django.urls import reverse, resolve
from task_manager.labels import views
from task_manager.labels.tests.settings_for_tests import SettingsLabels


class TestUrls(SettingsLabels):

    def test_labels_valid(self):
        url = reverse('labels')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Labels)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_list.html')


    def test_labels_unauthenticated_client(self):
        url = reverse('labels')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Labels)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_label_create_valid(self):
        url = reverse('create_label')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateLabel)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_user.html')


    def test_label_create_unauthenticated_user(self):
        url = reverse('create_label')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateLabel)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_label_update_valid(self):
        url = reverse('update_label', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateLabel)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_user.html')


    def test_label_update_unauthenticated_user(self):
        url = reverse('update_label', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateLabel)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_label_update_not_creator_user(self):
        url = reverse('update_label', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateLabel)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_label_delete_valid(self):
        url = reverse('delete_label', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteLabel)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_object_template.html')


    def test_label_delete_unauthenticated_user(self):
        url = reverse('delete_label', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteLabel)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_label_delete_not_creator_user(self):
        url = reverse('delete_label', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteLabel)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


