from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    """Task testcase object with options."""
    fixtures = ["test_users", "test_status", "test_labels", "test_tasks"]
    status_ok = HTTPStatus.OK

    def setUp(self) -> None:
        self.test_task_1 = Task.objects.get(pk=1)
        self.test_task_2 = Task.objects.get(pk=2)
        self.tasks = Task.objects.all()

        self.test_user_1 = User.objects.get(pk=2)
        self.test_user_2 = User.objects.get(pk=3)

        self.client.force_login(self.test_user_1)

        self.index_view = self.client.get(reverse_lazy("list_task"))
