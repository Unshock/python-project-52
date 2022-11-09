from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Task
from .setting import SettingsTasks


class TaskModelsTest(SettingsTasks):

    def test_models_params(self):
        self.assertEqual(self.test_task_id_1.name, "Test_task_1")
        self.assertEqual(
            self.test_task_id_1.creator.username, "user_authenticated")
        self.assertEqual(
            self.test_task_id_1.executor.last_name, "UserNotAdmin")
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(self.test_task_id_1.status.name, "Test_status_1")
        self.assertEqual(
            self.test_task_id_1._meta.get_field('name').verbose_name, _("Name"))

    def test_name_validation_fail(self):
        desciption_invalid = 'x' * 301
        task_invalid = Task(description=desciption_invalid,
                            creator_id=1, status_id=1)
        with self.assertRaises(ValidationError):
            task_invalid.full_clean()
            task_invalid.save()

    def test_unique_name_validation_fail(self):
        name_ununique = "Test_task_1"
        status_invalid = Task(name=name_ununique, creator_id=1, status_id=2)
        with self.assertRaises(ValidationError):
            status_invalid.full_clean()
            status_invalid.save()

    # def test_custom_getters(self):
    #     test_pk = 1
    #     test_task = Task.objects.get(id=test_pk)
    #     self.assertEqual(test_task.get_update_url(),
    #                      f'/tasks/{test_pk}/update/')
    #     self.assertEqual(test_task.get_delete_url(),
    #                      f'/tasks/{test_pk}/delete/')
