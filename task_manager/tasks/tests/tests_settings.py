from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status



class SettingsTasks(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = get_user_model()

        cls.client_auth = Client()
        cls.user_auth = user.objects.create(
            username="testuser",
            first_name="Test user f_n"
        )

        cls.user_auth.save()
        cls.client_auth.force_login(user.objects.last())

        cls.client_another = Client()
        cls.user_another = user.objects.create(
            username="testuser_another",
        )
        cls.user_another.save()
        cls.client_another.force_login(user.objects.last())

        cls.status_id1 = Status.objects.create(
            name="Test status 1",
            creator=cls.user_auth,
        )

        cls.status_id2 = Status.objects.create(
            name="Test status 2",
            creator=cls.user_auth,
        )

        cls.test_task_1 = Task.objects.create(
            name="Test_task_1",
            description="Do task_1",
            creator=cls.user_auth,
            executor=cls.user_another,
            status=cls.status_id1,
        )


