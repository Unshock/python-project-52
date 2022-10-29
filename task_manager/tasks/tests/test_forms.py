from task_manager.tasks.tests.settings_for_tests import SettingsTasks
from task_manager.tasks.forms import TaskForm


class TaskFormTest(SettingsTasks):

    def test_valid_form(self):
        form = TaskForm(data={
            'name': 'Test_task_4',
            'description': 'Test_task_4_description',
            'executor': self.user_authenticated_not_creator.id,
            'status': self.status_id_1.id,
        })

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TaskForm(data={
            'name': 'Testname' * 100,
            'description': 'Testdesc' * 300,
            'executor': self.user_authenticated_not_creator.username,
            'status': self.status_id_1.name,
            'labels': self.test_label_id_1.name
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)
