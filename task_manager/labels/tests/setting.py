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

        cls.client_authenticated_not_creator = Client()
        cls.user_authenticated_not_creator = user.objects.create(
            username="user_authenticated_not_creator",
            first_name="AuthenticatedNotCreator",
            last_name="UserNotAdmin"
        )
        cls.user_authenticated_not_creator.save()
        cls.client_authenticated_not_creator.force_login(user.objects.last())

        cls.client_unauthenticated = Client()
        cls.user_unauthenticated = user.objects.create(
            username="user_unauthenticated",
            first_name="NotAuthenticated",
            last_name="UserNotAdmin"
        )
        cls.user_unauthenticated.save()

        cls.label_id_1 = Label.objects.create(
            name="Test_label_1",
            creator=cls.user_authenticated,
        )

        cls.label_id_2 = Label.objects.create(
            name="Test_label_2",
            creator=cls.user_authenticated,
        )
