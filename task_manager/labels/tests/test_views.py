from http import HTTPStatus
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.labels.tests.settings_for_tests import SettingsLabels
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TestLabelViews(SettingsLabels):

    def setUp(self):
        self.list_url = reverse('labels')
        self.create_url = reverse('create_label')
        self.update_url = reverse('update_label', kwargs={'pk': 2})
        self.delete_url = reverse('delete_label', kwargs={'pk': 2})

    def test_label_list_GET(self):
        response = self.client_authenticated.get(self.list_url)
        label_list = response.context.get('label_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(label_list), 2)
        self.assertEqual(label_list[0].name, 'Test_label_1')
        self.assertEqual(label_list[1].id, 2)
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_label_list_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_label_GET(self):
        response = self.client_authenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context.get('page_title'), _('Create new label'))
        self.assertEqual(response.context.get('button_text'), _('Create'))
        self.assertTemplateUsed(response, 'base_create_and_update.html')

    def test_create_label_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_label_POST(self):
        self.assertEqual(Label.objects.all().count(), 2)

        label_data = {
            'name': 'Test_label_3'
        }

        response = self.client_authenticated.post(
            self.create_url, label_data)

        created_label = Label.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.all().count(), 3)
        self.assertEqual(created_label.name, 'Test_label_3')
        self.assertEqual(created_label.id, 3)
        self.assertEqual(created_label.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_create_label_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_label_GET(self):
        response = self.client_authenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Update label'))
        self.assertEqual(response.context.get('button_text'), _('Update'))
        self.assertTemplateUsed(response, 'base_create_and_update.html')

    def test_update_label_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_label_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_label_POST(self):
        self.assertEqual(Label.objects.all().count(), 2)

        label_data = {
            'name': 'Test_label_2_updated'
        }

        response = self.client_authenticated.post(
            self.update_url, label_data)

        updated_label = Label.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.all().count(), 2)
        self.assertEqual(updated_label.name, 'Test_label_2_updated')
        self.assertEqual(updated_label.id, 2)
        self.assertEqual(updated_label.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_update_label_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_label_POST_client_not_creator(self):

        label_data = {
            'name': 'Test_label_2_updated'
        }

        response = self.client_authenticated_not_creator.post(
            self.update_url, label_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.get(id=2).name, 'Test_label_2')

    def test_delete_label_GET(self):
        response = self.client_authenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Delete label'))
        self.assertEqual(response.context.get('button_text'), _('Delete'))
        self.assertTemplateUsed(response, 'base_delete.html')

    def test_delete_label_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_label_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_label_POST(self):
        self.assertEqual(Label.objects.all().count(), 2)

        response = self.client_authenticated.post(
            self.delete_url)

        last_label = Label.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.all().count(), 1)
        self.assertEqual(last_label.name, 'Test_label_1')
        self.assertEqual(last_label.id, 1)
        self.assertEqual(last_label.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_delete_used_label_POST(self):
        self.assertEqual(Label.objects.all().count(), 2)

        test_task = Task.objects.create(
            name='Test_task',
            description='Test_task_description',
            creator=self.user_authenticated,
            status=Status.objects.create(name='Test_status'))

        test_task.labels.add(self.label_id_2)
        test_task.save()

        response = self.client_authenticated.post(
            self.delete_url)

        last_label = Label.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.all().count(), 2)
        self.assertEqual(last_label.name, 'Test_label_2')
        self.assertEqual(last_label.id, 2)
        self.assertEqual(last_label.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_delete_label_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_label_POST_client_not_creator(self):

        response = self.client_authenticated_not_creator.post(
            self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.get(id=2).name, 'Test_label_2')
