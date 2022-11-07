from task_manager.labels.tests.setting import SettingsLabels
from task_manager.labels.forms import LabelForm


class LabelFormTest(SettingsLabels):

    def test_valid_creation_form(self):
        form = LabelForm(data={
            'name': 'Test_label_form_name',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_creation_form(self):
        form = LabelForm(data={
            'name': 'Test_label_form_name' * 100,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_empty_creation_form(self):
        form = LabelForm(data={
            'name': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
