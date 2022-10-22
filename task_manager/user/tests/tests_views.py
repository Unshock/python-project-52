from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from .settings_for_tests import SettingsUsers
from django.test import Client

from ..models import User


class UsersUrlsTest(SettingsUsers):

    def test_statuses_url(self):
        response = self.client_auth.get(reverse('users'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('users/user_list.html', response.template_name)

    def test_statuses_create_url(self):
        response = self.client_auth.get(reverse('create_user'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertTemplateUsed('create_user.html')

    def test_statuses_update_url(self):
        response = self.client_auth.get(
            reverse('update_user',
            kwargs={'user_id': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed(template_name='update_user.html')


    def test_statuses_update_url_unauth_user(self):
        response = self.client.get(
            reverse('update_user',
            kwargs={'user_id': 2})
        )

        self.assertEqual(response.status_code, 302)
        #with self.assertTemplateUsed('update_user.html'):
        #    render_to_string('update_user.html')
        #self.assertTemplateUsed('statuses/status_1list.html')

    def test_statuses_update_url_invalid_user(self):
        response = self.client_another.get(
            reverse('update_user',
            kwargs={'user_id': 1})
        )
        self.assertEqual(response.status_code, 302)


    def test_statuses_delete_url(self):
        response = self.client_auth.get(reverse('delete_user',
                                        kwargs={'user_id': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('delete_user.html', response.template_name)



    def test_statuses_delete_url_unauth_user(self):
        response = self.client.get(reverse('delete_user',
                                           kwargs={'user_id': 2}))
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)
        
    def test_statuses_delete_url_invalid_user(self):
        response = self.client_another.get(
            reverse('delete_user',
            kwargs={'user_id': 1})
        )
        self.assertEqual(response.status_code, 302)
        #self.assertIn('delete_user.html', response.template_name)



class StatusesViewTest(SettingsUsers):

    def test_users_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Users list')
        users_list = response.context.get('users_list')
        self.assertEqual(len(users_list), 2)
        self.assertEqual(users_list[0].username, 'testuser')
        self.assertEqual(users_list[1].username, 'testuser_another')
        self.assertEqual(users_list[1].last_name, 'Smith')

    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('create_user.html', response.template_name)
        self.assertEqual(response.context.get('title'), 'User creation')
        self.assertEqual(response.context.get('action'), 'Create new user')
        self.assertEqual(response.context.get('button_text'), 'Create')

    def test_update_user_get(self):
        test_pk = 1
        response = self.client_auth.get(
            reverse('update_user',
                    kwargs={'user_id': test_pk}
                    )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('title'), 'Update user')
        self.assertEqual(response.context.get('action'), 'Update user')
        self.assertEqual(response.context.get('button_text'), 'Update')

    def test_delete_user_get(self):
        test_pk = 1
        response = self.client_auth.get(
            reverse('delete_user',
            kwargs={'user_id': test_pk}
                    )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # with self.assertTemplateUsed('update_user.html'):
        #     render_to_string('update_user.html')
        self.assertEqual(response.context.get('title'), 'Delete user')
        self.assertEqual(response.context.get('action'), 'Delete user')
        self.assertEqual(response.context.get('button_text'), 'Delete')

    def test_delete_user_post(self):

        form_data = {
            'name': 'teststatus5'
        }

        create_response = self.client_auth.post(
            reverse('create_status'),
            data=form_data,
            follow=True
        )
        created_object = Status.objects.last()
        self.assertEqual(Status.objects.count(), 1)

        delete_response = self.client_auth.post(
            reverse('delete_status',
            kwargs={'status_id': created_object.pk})
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)

    def test_delete_user_post2(self):

        user_count_before = User.objects.count()
        self.assertEqual(user_count_before, 2)

        create_form_data = {
            'username': 'New_user',
            'first_name': 'John',
            'last_name': 'Novichek',
            'password1': 'qweR19Tyui',
            'password2': 'qweR19Tyui'
        }

        client_new = Client()
        create_response = self.client.post(
            reverse('create_user'),
            data=create_form_data,
            follow=True
        )

        user_new = User.objects.last()
        client_new.force_login(user_new)

        created_object = User.objects.last()
        user_count_after = User.objects.count()

        self.assertEqual(user_count_after, 3)
        self.assertEqual(created_object.pk, 3)

        response = client_new.post(
            reverse('delete_user', kwargs={'user_id': created_object.pk}),
            follow=True
        )

        user_count_after = User.objects.count()
        last_object = User.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(user_count_after, 2)
        self.assertEqual(last_object.id, 2)
        self.assertEqual(last_object.username, "testuser_another")
        self.assertEqual(last_object.first_name, "Another")
        self.assertEqual(last_object.last_name, "Smith")
        self.assertTrue(last_object.password)
