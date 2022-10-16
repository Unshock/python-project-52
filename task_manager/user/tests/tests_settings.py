from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from task_manager.statuses.models import Status



class SettingsUsers(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = get_user_model()

        cls.client_auth = Client()
        cls.user_auth = user.objects.create(
            username="testuser",
            first_name="Aaron",
            last_name="Test"
        )

        cls.user_auth.save()
        cls.client_auth.force_login(user.objects.last())

        cls.client_another = Client()
        cls.user_another = user.objects.create(
            username="testuser_another",
            first_name="Another",
            last_name="Smith",
            password="QWERTY123uiop",
        )
        cls.user_another.save()
        cls.client_another.force_login(user.objects.last())
