from task_manager.tasks.tests.settings_for_tests import SettingsTasks
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task


class TestTasksViews(SettingsTasks):

    def setUp(self):
        self.qs = Task.objects.all()
        self.filter = TaskFilter(queryset=self.qs,
                                 user=self.user_authenticated)

    def test_task_filter_self_tasks(self):
        self.assertEqual(self.qs.count(), 3)

        filter = TaskFilter(
            data={'self_tasks': True},
            queryset=self.qs,
            user=self.user_authenticated_not_creator)

        self.assertEqual(filter.qs.count(), 1)
        self.assertEqual(filter.qs.first().name, 'Test_task_3')
        self.assertEqual(filter.qs.last().creator_id, 2)

        filter = TaskFilter(
            data={'self_tasks': False},
            queryset=self.qs,
            user=self.user_authenticated_not_creator)

        self.assertEqual(filter.qs.count(), 3)
        self.assertEqual(filter.qs.first().name, 'Test_task_1')
        self.assertEqual(filter.qs.last().creator_id, 2)

    def test_task_filter_by_status_1(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_status(
            self.qs, 'status', self.status_id_2)

        self.assertEqual(result.count(), 2)
        self.assertEqual(result.first().name, 'Test_task_2')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_by_status_2(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_status(
            self.qs, 'status', self.status_id_1)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().name, 'Test_task_1')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated')

    def test_task_filter_by_status_3(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_status(
            self.qs, 'status', value=None)

        self.assertEqual(result.count(), 3)
        self.assertEqual(result.first().name, 'Test_task_1')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_by_label_1(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_label(
            self.qs, 'label', self.test_label_id_1)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().name, 'Test_task_2')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated')

    def test_task_filter_by_label_2(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_label(
            self.qs, 'label', self.test_label_id_2)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().name, 'Test_task_3')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_by_label_3(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_label(
            self.qs, 'label', value=None)

        self.assertEqual(result.count(), 3)
        self.assertEqual(result.first().name, 'Test_task_1')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_by_executor_1(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_executor(
            self.qs, 'executor', self.user_authenticated)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().name, 'Test_task_2')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated')

    def test_task_filter_by_executor_2(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_executor(
            self.qs, 'executor', self.user_authenticated_not_creator)

        self.assertEqual(result.count(), 2)
        self.assertEqual(result.first().name, 'Test_task_1')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_by_executor_3(self):
        self.assertEqual(self.qs.count(), 3)

        result = self.filter.filter_by_executor(
            self.qs, 'executor', value=None)

        self.assertEqual(result.count(), 3)
        self.assertEqual(result.first().name, 'Test_task_1')
        self.assertEqual(result.last().creator.username,
                         'user_authenticated_not_creator')

    def test_task_filter_several_filters(self):
        self.assertEqual(self.qs.count(), 3)

        result_1 = self.filter.filter_by_executor(
            self.qs, 'executor', self.user_authenticated_not_creator)
        result_2 = self.filter.filter_by_label(
            result_1, 'label', self.test_label_id_2
        )
        result_final = self.filter.filter_by_status(
            result_2, 'status', self.status_id_2
        )

        self.assertEqual(result_final.count(), 1)
        self.assertEqual(result_final.first().name, 'Test_task_3')
        self.assertEqual(result_final.last().creator.username,
                         'user_authenticated_not_creator')
