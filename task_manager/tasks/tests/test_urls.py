from http import HTTPStatus
from django.urls import reverse, resolve

from task_manager.tasks.tests.settings_for_tests import SettingsTasks
from task_manager.tasks import views


class TestUrls(SettingsTasks):

    def test_tasks_valid(self):
        url = reverse('tasks')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Tasks)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_tasks_unauthenticated_client(self):
        url = reverse('tasks')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.Tasks)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_task_create_valid(self):
        url = reverse('create_task')
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateTask)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/create_task.html')


    def test_task_create_unauthenticated_user(self):
        url = reverse('create_task')

        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.CreateTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_task_update_valid(self):
        url = reverse('update_task', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateTask)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/create_task.html')


    def test_task_update_unauthenticated_user(self):
        url = reverse('update_task', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_task_update_not_creator_user(self):
        url = reverse('update_task', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.UpdateTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_task_delete_valid(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteTask)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_user.html')


    def test_task_delete_unauthenticated_user(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


    def test_task_delete_not_creator_user(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        response = self.client_authenticated_not_creator.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DeleteTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_task_detail(self):
        url = reverse('detail_task', kwargs={'pk': 1})
        response = self.client_authenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DetailTask)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/detail_task.html')

    def test_task_detail_unauthenticated_client(self):
        url = reverse('detail_task', kwargs={'pk': 1})
        response = self.client_unauthenticated.get(url)

        self.assertEqual(resolve(url).func.view_class, views.DetailTask)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
