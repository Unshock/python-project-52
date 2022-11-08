from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from .setting import SettingsStatuses


class StatusesModelsTest(SettingsStatuses):

    def test_models_params(self):
        self.assertEqual(self.status_id_1.name, "Test_status_1")
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(self.status_id_1._meta.get_field('name').verbose_name,
                         _("Name"))

    def test_name_validation_fail(self):
        name_invalid = 'x' * 101
        status_invalid = Status(name=name_invalid)
        with self.assertRaises(ValidationError):
            status_invalid.full_clean()
            status_invalid.save()

    def test_unique_name_validation_fail(self):
        name_ununique = "Test_status_1"
        status_invalid = Status(name=name_ununique)
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
