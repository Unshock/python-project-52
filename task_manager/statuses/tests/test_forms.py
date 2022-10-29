from task_manager.statuses.tests.settings_for_tests import SettingsStatuses
from task_manager.statuses.forms import StatusForm


class StatusFormTest(SettingsStatuses):

    def test_valid_creation_form(self):
        form = StatusForm(data={
            'name': 'Test_status_form_name',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_creation_form(self):
        form = StatusForm(data={
            'name': 'Test_status_form_name' * 100,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_empty_creation_form(self):
        form = StatusForm(data={
            'name': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
