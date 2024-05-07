from django.urls import reverse_lazy

from task_manager.tasks.tests.task_test_case import TaskTestCase


class TestTasksIndexViews(TaskTestCase):

    def test_list_view_returns_correct_response(self) -> None:
        test_response = self.client.get(reverse_lazy("list_task"))

        self.assertEqual(test_response.status_code, self.status_ok)
        self.assertTemplateUsed(test_response, "list_objects.html")

    # def test_list_view_contains_correct_fields(self) -> None:
