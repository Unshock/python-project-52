from http import HTTPStatus
from django.urls import reverse
from task_manager.statuses.models import Status
from .tests_settings import SettingsStatuses



class StatusFormTest(SettingsStatuses):
    def test_valid_creation_form(self):
        status_count_before = Status.objects.count()

        form_data = {
            'name': 'teststatus3'
        }

        response = self.client_auth.post(
            reverse('create_status'),
            data=form_data,
            follow=True
        )

        status_count_after = Status.objects.count()
        created_object = Status.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(status_count_before + 1, status_count_after)
        self.assertEqual(status_count_after, 3)
        self.assertEqual(created_object.id, 3)
        self.assertEqual(created_object.name, "teststatus3")
        self.assertEqual(created_object.creator_id, 1)


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
        status_count_before = Status.objects.count()

        create_form_data = {
            'name': 'teststatus3'
        }

        self.client_auth.post(reverse('create_status'),
                              data=create_form_data,
                              follow=True
                              )

        created_object = Status.objects.last()

        update_form_data = {
            'name': 'teststatus3-updated'
        }

        response = self.client_auth.post(
            reverse('update_status', kwargs={'status_id': created_object.pk}),
            data=update_form_data,
            follow=True
        )

        status_count_after = Status.objects.count()
        created_object = Status.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(status_count_before + 1, status_count_after)
        self.assertEqual(status_count_after, 3)
        self.assertEqual(created_object.id, 3)
        self.assertEqual(created_object.name, "teststatus3-updated")
        self.assertEqual(created_object.creator_id, 1)

    def test_invalid_update_form(self):
        status_count_before = Status.objects.count()

        create_form_data = {
            'name': 'teststatus3'
        }

        self.client_auth.post(reverse('create_status'),
                              data=create_form_data,
                              follow=True
                              )

        created_object = Status.objects.last()

        invalid_update_form_data = {
            'name': 'x' * 101
        }

        response = self.client_auth.post(
            reverse('update_status', kwargs={'status_id': created_object.pk}),
            data=invalid_update_form_data,
            follow=True
        )

        status_count_after = Status.objects.count()
        created_object = Status.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(status_count_before + 1, status_count_after)
        self.assertEqual(status_count_after, 3)
        self.assertEqual(created_object.id, 3)
        self.assertEqual(created_object.name, "teststatus3")
        self.assertEqual(created_object.creator_id, 1)
