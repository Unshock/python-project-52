from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from .tests_settings import SettingsStatuses
from ..forms import CreateStatusForm


class StatusesUrlsTest(SettingsStatuses):

    def test_statuses_url(self):
        response = self.client_auth.get(reverse('statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('statuses/status_list.html', response.template_name)

    def test_statuses_create_url(self):
        response = self.client_auth.get(reverse('create_status'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertTemplateUsed('create_user.html')

    def test_statuses_update_url(self):
        response = self.client_auth.get(reverse('update_status',
                                           kwargs={'status_id': 2}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed(template_name='update_user.html')


    def test_statuses_update_url_unauth_user(self):
        response = self.client.get(reverse('update_status',
                                           kwargs={'status_id': 2}))

        self.assertEqual(response.status_code, 302)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed('statuses/status_1list.html')

    def test_statuses_update_url_invalid_user(self):
        response = self.client_another.get(
            reverse('update_status',
            kwargs={'status_id': 2})
        )
        self.assertEqual(response.status_code, 302)

    def test_statuses_delete_url(self):
        response = self.client_auth.get(reverse('delete_status',
                                        kwargs={'status_id': 2}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('delete_user.html', response.template_name)



    def test_statuses_delete_url_unauth_user(self):
        response = self.client.get(reverse('delete_status',
                                           kwargs={'status_id': 2}))
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)
        
    def test_statuses_delete_url_invalid_user(self):
        response = self.client_another.get(
            reverse('delete_status',
            kwargs={'status_id': 2})
        )
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)



class StatusesViewTest(SettingsStatuses):

    def test_statuses_list(self):
        response = self.client_auth.get(reverse('statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Statuses list')
        statuses_list = response.context.get('statuses_list')
        self.assertEqual(len(statuses_list), 2)
        self.assertEqual(statuses_list[0].name, 'Test status 1')

    def test_statuses_list_user_is_not_authenticated(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_create_status(self):
        # self.assertEqual(self.status1.name, "Test status 1")
        # self.assertEqual(self.status2.creator.username, "Test user")
        # self.assertEqual(len(Status.objects.all()), 2)
        # self.assertEqual(self.status2.creator.last_name, "")
        # self.assertEqual(self.status1._meta.get_field('name').verbose_name,
        #                  "Имя статуса")
        print('views_---------------------')
        response = self.client_auth.get(reverse('create_status'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('create_user.html', response.template_name)
        self.assertEqual(response.context.get('title'), 'Status creation')
        self.assertEqual(response.context.get('action'), 'Create new status')
        self.assertEqual(response.context.get('button_text'), 'Create')
        #self.assertEqual(response.context.get('form'), CreateStatusForm)
        #print(1, response.context.get('form'))
        #print(type(response.context.get('form')))
  #       self.assertEqual(response.context.get('form'), """<tr>
  #   <th><label for="id_name">Имя:</label></th>
  #   <td>
  #     <input type="text" name="name" class="form-control" required id="id_name">
  #   </td>
  # </tr>""")
    def test_update_status_get(self):
        test_pk = 2
        # response = self.client.get(reverse('update_status',
        #                                    kwargs={'status_id': test_pk}),
        #                            kwargs={'user_id': 2})
        response = self.client_auth.get(reverse('update_status',
                                           kwargs={'status_id': test_pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('create_user.html', response.context.template_name)
        self.assertEqual(response.context.get('title'), 'Update status')
        self.assertEqual(response.context.get('action'), 'Update')
        self.assertEqual(response.context.get('button_text'), 'Update')


    def test_delete_status_get(self):
        test_pk = 2
        response = self.client_auth.get(reverse('delete_status',
                                           kwargs={'status_id': test_pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # with self.assertTemplateUsed('update_user.html'):
        #     render_to_string('update_user.html')
        self.assertEqual(response.context.get('title'), 'Delete status')
        self.assertEqual(response.context.get('action'), 'Delete status')
        self.assertEqual(response.context.get('button_text'), 'Delete')

    def test_delete_status_post(self):

        form_data = {
            'name': 'teststatus5'
        }

        create_response = self.client_auth.post(
            reverse('create_status'),
            data=form_data,
            follow=True
        )
        created_object = Status.objects.last()
        self.assertEqual(Status.objects.count(), 3)

        delete_response = self.client_auth.post(
            reverse('delete_status',
            kwargs={'status_id': created_object.pk})
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)
