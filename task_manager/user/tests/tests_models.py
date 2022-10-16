from django.core.exceptions import ValidationError
from django.urls import reverse

from task_manager.statuses.models import Status
from .tests_settings import SettingsUsers
from ..models import User


class UsersModelsTest(SettingsUsers):

    def test_models_params(self):
        self.assertEqual(self.user_auth.username, "testuser")
        self.assertEqual(self.user_auth.first_name, "Aaron")
        self.assertEqual(self.user_auth.last_name, "Test")
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.user_another._meta.get_field('creation_date').verbose_name,
                         "Дата создания")

    def test_username_validation_fail(self):
        username_invalid = 'x$'
        user_invalid = User(username=username_invalid,
                              first_name='A',
                              last_name='B',
                              password="qwerty123UIOP"
                              )
        with self.assertRaises(ValidationError):
            user_invalid.full_clean()
            user_invalid.save()


    def test_unique_name_validation_fail(self):
        name_ununique = "testuser"
        user_invalid = User(username=name_ununique,
                            first_name='A',
                            last_name='B',
                            password="qwerty123UIOP"
                            )
        with self.assertRaises(ValidationError):
            user_invalid.full_clean()
            user_invalid.save()


    def test_custom_getters(self):
        test_pk = 1
        test_user = User.objects.get(id=test_pk)
        self.assertEqual(test_user.get_update_url(),
                         f'/users/{test_pk}/update/')
        self.assertEqual(test_user.get_delete_url(),
                         f'/users/{test_pk}/delete/')
        self.assertEqual(
            test_user.get_update_url(),
            reverse('update_user', kwargs={"user_id": test_pk})
        )
        self.assertEqual(
            test_user.get_delete_url(),
            reverse('delete_user', kwargs={"user_id": test_pk})
        )
