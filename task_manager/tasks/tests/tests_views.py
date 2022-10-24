from http import HTTPStatus
from django.urls import reverse
from task_manager.statuses.models import Status
from .settings_for_tests import SettingsTasks
from ..models import Task


class TestTasksViews(SettingsTasks):

    def setUp(self):
        self.list_url = reverse('tasks')
        self.create_url = reverse('create_task')
        self.update_url = reverse('update_task', kwargs={'pk': 1})
        self.delete_url = reverse('delete_task', kwargs={'pk': 1})
        self.detail_url = reverse('detail_task', kwargs={'pk': 1})

    def test_task_list_GET(self):

        response = self.client_authenticated.get(self.list_url)
        tasks = response.context.get('tasks')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Task list')
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].name, 'Test_task_1')
        self.assertEqual(tasks[0].creator.username, 'user_authenticated')
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_list_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_task_GET(self):
        response = self.client_authenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Task creation')
        self.assertEqual(response.context.get('action'), 'Create new task')
        self.assertEqual(response.context.get('button_text'), 'Create')
        self.assertTemplateUsed(response, 'tasks/create_task.html')

    def test_create_task_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_task_POST(self):
        self.assertEqual(Task.objects.all().count(), 3)

        task_data = {
            'name': 'Test_task_4',
            'description': 'Test_task_4_description',
            'status': self.status_id_2.id,
            'labels': self.test_label_id_1.id
        }

        response = self.client_authenticated.post(
            self.create_url, task_data)

        created_task = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.all().count(), 4)
        self.assertEqual(created_task.name, 'Test_task_4')
        self.assertEqual(created_task.id, 4)
        self.assertEqual(created_task.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_create_task_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_task_GET(self):
        response = self.client_authenticated.get(self.update_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Update task')
        self.assertEqual(response.context.get('action'), 'Update task')
        self.assertEqual(response.context.get('button_text'), 'Update')
        #self.assertEqual(response.initial.get('labels'), self.status_id_1)
        self.assertTemplateUsed(response, 'tasks/create_task.html')

    def test_update_task_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_task_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_task_POST(self):
        self.assertEqual(Task.objects.all().count(), 3)

        task_data = {
            'name': 'Test_task_1_updated',
            'description': 'Test_task_1_description_updated',
            'status': self.status_id_2.id,
            'labels': self.test_label_id_1.id
        }

        response = self.client_authenticated.post(
            self.update_url, task_data)

        updated_task = Task.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.all().count(), 3)
        self.assertEqual(updated_task.name, 'Test_task_1_updated')
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.creator.username, 'user_authenticated')
        self.assertRedirects(response, self.list_url)

    def test_update_task_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.update_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_task_POST_client_not_creator(self):

        task_data = {
            'name': 'Test_task_1_updated',
            'description': 'Test_task_1_description_updated',
            'status': self.status_id_2.id,
            'labels': self.test_label_id_1.id
        }

        response = self.client_authenticated_not_creator.post(
            self.update_url, task_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.get(id=1).name, 'Test_status_1')

    def test_delete_task_GET(self):
        response = self.client_authenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Delete task')
        self.assertEqual(response.context.get('action'), 'Delete task')
        self.assertEqual(response.context.get('button_text'), 'Delete')
        self.assertTemplateUsed(response, 'delete_user.html')

    def test_delete_task_GET_unauthenticated_client(self):
        response = self.client_unauthenticated.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_task_GET_client_not_creator(self):
        response = self.client_authenticated_not_creator.get(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_task_POST(self):
        self.assertEqual(Task.objects.all().count(), 3)

        response = self.client_authenticated.post(
            self.delete_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.all().count(), 2)
        self.assertRedirects(response, self.list_url)

    def test_delete_task_POST_unauthenticated_client(self):
        response = self.client_unauthenticated.post(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_task_POST_client_not_creator(self):
        response = self.client_authenticated_not_creator.post(
            self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.get(id=1).name, 'Test_task_1')
