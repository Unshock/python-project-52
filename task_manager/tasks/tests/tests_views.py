from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from .tests_settings import SettingsTasks
from ..models import Task


class TasksUrlsTest(SettingsTasks):

    def test_tasks_url(self):
        response = self.client_auth.get(reverse('tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('tasks/task_list.html', response.template_name)

    def test_tasks_create_url(self):
        response = self.client_auth.get(reverse('create_task'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertTemplateUsed('create_user.html')

    def test_tasks_update_url(self):
        response = self.client_auth.get(reverse('update_task',
                                           kwargs={'pk': 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed(template_name='update_user.html')


    def test_tasks_update_url_unauth_user(self):
        response = self.client.get(reverse('update_task',
                                           kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 302)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed('statuses/status_1list.html')

    def test_tasks_update_url_invalid_user(self):
        response = self.client_another.get(
            reverse('update_task',
            kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_tasks_delete_url(self):
        response = self.client_auth.get(reverse('delete_task',
                                        kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('delete_user.html', response.template_name)



    def test_tasks_delete_url_unauth_user(self):
        response = self.client.get(reverse('delete_task',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)
        
    def test_tasks_delete_url_invalid_user(self):
        response = self.client_another.get(
            reverse('delete_task',
            kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)



class StatusesViewTest(SettingsTasks):

    def test_tasks_list(self):
        response = self.client_auth.get(reverse('tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Task list')
        tasks_list = response.context.get('task_list')
        self.assertEqual(len(tasks_list), 1)
        self.assertEqual(tasks_list[0].name, 'Test_task_1')

    def test_tasks_list_user_is_not_authenticated(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_create_tasks(self):

        response = self.client_auth.get(reverse('create_task'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('create_user.html', response.template_name)
        self.assertEqual(response.context.get('title'), 'Task creation')
        self.assertEqual(response.context.get('action'), 'Create new task')
        self.assertEqual(response.context.get('button_text'), 'Create')
        #self.assertEqual(response.context.get('form'), CreateStatusForm)

    def test_update_tasks_get(self):
        test_pk = 1

        response = self.client_auth.get(
            reverse('update_task',
            kwargs={'pk': test_pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('create_user.html', response.context.template_name)
        self.assertEqual(response.context.get('title'), 'Update task')
        self.assertEqual(response.context.get('action'), 'Update task')
        self.assertEqual(response.context.get('button_text'), 'Update')


    def test_delete_tasks_get(self):
        test_pk = 1
        response = self.client_auth.get(reverse('delete_task',
                                           kwargs={'pk': test_pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # with self.assertTemplateUsed('update_user.html'):
        #     render_to_string('update_user.html')
        self.assertEqual(response.context.get('title'), 'Delete task')
        self.assertEqual(response.context.get('action'), 'Delete task')
        self.assertEqual(response.context.get('button_text'), 'Delete')

    def test_delete_tasks_post(self):

        form_data = {
            'name': 'task_to_del',
            'description': 'desc_task',
            'status': self.status_id1.id,
        }

        response = self.client_auth.post(
            reverse('create_task'),
            data=form_data,
            follow=True
        )

        created_object = Task.objects.last()
        self.assertEqual(Task.objects.count(), 2)

        delete_response = self.client_auth.post(
            reverse('delete_task',
            kwargs={'pk': created_object.pk})
        )

        self.assertEqual(delete_response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)
