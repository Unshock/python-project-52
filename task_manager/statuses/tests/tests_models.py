from django.core.exceptions import ValidationError
from task_manager.statuses.models import Status
from .tests_settings import SettingsStatuses


class StatusesModelsTest(SettingsStatuses):

    def test_models_params(self):
        self.assertEqual(self.status_id1.name, "Test status 1")
        self.assertEqual(self.status_id2.creator.username, "testuser")
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(self.status_id2.creator.last_name, "")
        self.assertEqual(self.status_id1._meta.get_field('name').verbose_name,
                         "Имя статуса")

    def test_name_validation_fail(self):
        name_invalid = 'x' * 101
        status_invalid = Status(name=name_invalid, creator_id=1)
        with self.assertRaises(ValidationError):
            status_invalid.full_clean()
            status_invalid.save()


    def test_unique_name_validation_fail(self):
        name_ununique = "Test status 1"
        status_invalid = Status(name=name_ununique, creator_id=1)
        with self.assertRaises(ValidationError):
            status_invalid.full_clean()
            status_invalid.save()


    def test_custom_getters(self):
        test_pk = 2
        test_status = Status.objects.get(id=test_pk)
        self.assertEqual(test_status.get_update_url(),
                         f'/statuses/{test_pk}/update/')
        self.assertEqual(test_status.get_delete_url(),
                         f'/statuses/{test_pk}/delete/')
