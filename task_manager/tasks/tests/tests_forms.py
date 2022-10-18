from http import HTTPStatus
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from .tests_settings import SettingsTasks
from ..forms import CreateTaskForm


class TaskFormTest(SettingsTasks):
    
    def test_valid_form(self):
        form = CreateTaskForm(data={
            'name': 'Testname',
            'description': 'Testdesc',
            'executor': self.user_another.id,
            'status': self.status_id1.id,
        })
        
        #print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CreateTaskForm(data={
            'name': 'Testname'*100,
            'description': 'Testdesc'*300,
            'executor': self.user_another.username,
            'status': self.status_id1.name,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


    def test_valid_creation_form(self):
        tasks_count_before = Task.objects.count()

        form_data = {
            'name': 'testtask3',
            'description': 'desc1',
            'executor': self.user_another.id,
            'status': self.status_id1.id,
        }


        response = self.client_auth.post(
            reverse('create_task'),
            data=form_data,
            follow=True
        )

        tasks_count_after = Task.objects.count()
        created_object = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(tasks_count_before + 1, tasks_count_after)
        self.assertEqual(tasks_count_after, 2)
        self.assertEqual(created_object.id, 2)
        self.assertEqual(created_object.name, "testtask3")
        self.assertEqual(created_object.executor_id, 2)
        self.assertEqual(created_object.creator_id, 1)
        self.assertEqual(created_object.status_id, 1)


    def test_invalid_creation_form(self):

        status_count_before = Status.objects.count()

        form_data = {
            'name': 'x'*101
        }

        response = self.client_auth.post(
            reverse('create_status'),
            data=form_data,
            follow=True
        )

        status_count_after = Status.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(status_count_before, status_count_after)
        self.assertEqual(status_count_after, 2)


    def test_valid_update_form(self):
        tasks_count_before = Task.objects.count()

        form_data = {
            'name': 'testtask3-updated',
            'description': 'desc1-updated',
            'executor': self.user_auth.id,
            'status': self.status_id1.id,
        }

        created_object = Task.objects.last()

        response = self.client_auth.post(
            reverse('update_task', kwargs={'pk': created_object.pk}),
            data=form_data,
            follow=True
        )

        tasks_count_after = Task.objects.count()
        created_object = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(tasks_count_after, 1)
        self.assertEqual(created_object.id, 1)
        self.assertEqual(created_object.name, "testtask3-updated")
        self.assertEqual(created_object.description, "desc1-updated")
        self.assertEqual(created_object.executor.username, "testuser")
        self.assertEqual(created_object.status.name, "Test status 1")
        self.assertEqual(created_object.executor_id, 1)
        self.assertEqual(created_object.creator_id, 1)
        self.assertEqual(created_object.status_id, 1)

    def test_invalid_update_form(self):
        tasks_count_before = Task.objects.count()

        form_data = {
            'name': 'testtask3-updated',
            'description': 'desc1-updated',
            'executor': self.user_auth.id,
            'status': self.status_id1.name,
        }

        created_object = Task.objects.last()

        response = self.client_auth.post(
            reverse('update_task', kwargs={'pk': created_object.pk}),
            data=form_data,
            follow=True
        )

        print(tasks_count_before)

        status_count_after = Task.objects.count()
        created_object = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(status_count_after, 1)
        self.assertEqual(created_object.id, 1)
        self.assertEqual(created_object.name, "Test_task_1")
        self.assertEqual(created_object.creator_id, 1)
