from django.core.exceptions import ValidationError
from task_manager.labels.tests.setting import SettingsLabels
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class LabelModelsTest(SettingsLabels):

    def test_models_params(self):
        self.assertEqual(self.label_id_1.name, "Test_label_1")
        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(self.label_id_1._meta.get_field('name').verbose_name,
                         "Имя метки")

    def test_name_validation_fail(self):
        name_invalid = 'x' * 101
        label_invalid = Label(name=name_invalid)
        with self.assertRaises(ValidationError):
            label_invalid.full_clean()
            label_invalid.save()

    def test_unique_name_validation_fail(self):
        name_ununique = "Test_label_1"
        label_invalid = Task(name=name_ununique)
        with self.assertRaises(ValidationError):
            label_invalid.full_clean()
            label_invalid.save()

    def test_custom_getters(self):
        test_pk = 1
        test_label = Label.objects.get(id=test_pk)
        self.assertEqual(test_label.get_update_url(),
                         f'/labels/{test_pk}/update/')
        self.assertEqual(test_label.get_delete_url(),
                         f'/labels/{test_pk}/delete/')
