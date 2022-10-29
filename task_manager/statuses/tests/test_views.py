from http import HTTPStatus
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.statuses.tests.settings_for_tests import SettingsStatuses
from task_manager.tasks.models import Task


class TestStatusesViews(SettingsStatuses):

    def setUp(self):
        self.list_url = reverse('statuses')
        self.create_url = reverse('create_status')
        self.update_url = reverse('update_status', kwargs={'pk': 2})
        self.delete_url = reverse('delete_status', kwargs={'pk': 2})

    def test_status_list_GET(self):

        response = self.client_authenticated.get(self.list_url)
        status_list = response.context.get('status_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(status_list), 2)
        self.assertEqual(status_list[0].name, 'Test_status_1')
        self.assertEqual(status_list[1].id, 2)
        self.assertTemplateUsed(response, 'statuses/status_list.html')

    def test_status_list_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_status_GET(self):
        response = self.client_authenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context.get('page_title'), _('Create new status'))
        self.assertEqual(response.context.get('button_text'), _('Create'))
        self.assertTemplateUsed(response, 'create_user.html')

    def test_create_status_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_status_POST(self):
        self.assertEqual(Status.objects.all().count(), 2)

        status_data = {
            'name': 'Test_status_3'
        }

        response = self.client_authenticated.post(
            self.create_url, status_data)

        created_status = Status.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.all().count(), 3)
        self.assertEqual(created_status.name, 'Test_status_3')
        self.assertEqual(created_status.id, 3)
        self.assertEqual(created_status.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_create_status_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_status_GET(self):
        response = self.client_authenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Update status'))
        self.assertEqual(response.context.get('button_text'), _('Update'))
        self.assertTemplateUsed(response, 'update_user.html')

    def test_update_status_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_status_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_status_POST(self):
        self.assertEqual(Status.objects.all().count(), 2)

        status_data = {
            'name': 'Test_status_2_updated'
        }

        response = self.client_authenticated.post(
            self.update_url, status_data)

        updated_status = Status.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.all().count(), 2)
        self.assertEqual(updated_status.name, 'Test_status_2_updated')
        self.assertEqual(updated_status.id, 2)
        self.assertEqual(updated_status.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_update_status_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_status_POST_client_not_creator(self):

        status_data = {
            'name': 'Test_status_2_updated'
        }

        response = self.client_authenticated_not_creator.post(
            self.update_url, status_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.get(id=2).name, 'Test_status_2')

    def test_delete_status_GET(self):
        response = self.client_authenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('page_title'), _('Delete status'))
        self.assertEqual(response.context.get('button_text'), _('Delete'))
        self.assertTemplateUsed(response, 'delete_object_template.html')

    def test_delete_status_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_status_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_status_POST(self):
        self.assertEqual(Status.objects.all().count(), 2)

        response = self.client_authenticated.post(
            self.delete_url)

        last_status = Status.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.all().count(), 1)
        self.assertEqual(last_status.name, 'Test_status_1')
        self.assertEqual(last_status.id, 1)
        self.assertEqual(last_status.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_delete_used_status_POST(self):
        self.assertEqual(Status.objects.all().count(), 2)

        test_task = Task.objects.create(
            name='Test_task',
            description='Test_task_description',
            creator=self.user_authenticated,
            status=self.status_id_2
        )

        test_task.save()

        response = self.client_authenticated.post(
            self.delete_url)

        last_status = Status.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.all().count(), 2)
        self.assertEqual(last_status.name, 'Test_status_2')
        self.assertEqual(last_status.id, 2)
        self.assertEqual(last_status.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_delete_status_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_status_POST_client_not_creator(self):
        response = self.client_authenticated_not_creator.post(
            self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.get(id=2).name, 'Test_status_2')
