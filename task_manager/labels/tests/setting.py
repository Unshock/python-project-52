from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from task_manager.labels.models import Label


class SettingsLabels(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = get_user_model()

        cls.client_authenticated = Client()
        cls.user_authenticated = user.objects.create(
            username="user_authenticated",
            first_name="Authenticated",
            last_name="UserNotAdmin"
        )
        cls.user_authenticated.save()
        cls.client_authenticated.force_login(user.objects.last())

        cls.client_unauthenticated = Client()
        cls.user_unauthenticated = user.objects.create(
            username="user_unauthenticated",
            first_name="NotAuthenticated",
            last_name="UserNotAdmin"
        )
        cls.user_unauthenticated.save()

        cls.label_id_1 = Label.objects.create(
            name="Test_label_1",
        )

        cls.label_id_2 = Label.objects.create(
            name="Test_label_2",
        )
