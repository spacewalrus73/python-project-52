from http import HTTPStatus

from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tasks.views import TaskCreateView
from task_manager.users.models import User


class TaskIndexTest(MessagesTestMixin, TestCase):
    """Test tasks list. Authentication required."""

    fixtures: list = ["test_users", "test_status", "test_tasks"]

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(reverse_lazy("list_task"))

    def test_list_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "tasks_table.html")

    def test_list_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "ID")
        self.assertContains(self.view_response, "Name")
        self.assertContains(self.view_response, "Status")
        self.assertContains(self.view_response, "Author")
        self.assertContains(self.view_response, "Performer")
        self.assertContains(self.view_response, "Creation date")
        self.assertContains(self.view_response, "Tasks")
        self.assertContains(self.view_response, "Create task")
        self.assertContains(self.view_response, "Show")
        # data from fixtures
        self.assertContains(self.view_response, "Task1")
        self.assertContains(self.view_response, "Task2")
        self.assertContains(self.view_response, "TestStatus")
        self.assertContains(self.view_response, "SecondStatus")
        self.assertContains(self.view_response, "Linus Torvalds")
        self.assertContains(self.view_response, "Guido Van Rossum")

    # def test_filter_task(self):
    #     filter_response = self.client.post(
    #         path=reverse_lazy(viewname="list_task",
    #                           kwargs={"status": Status.objects.first().id,
    #                                   "performer": User.objects.first().id}),
    #         follow=True,
    #     )
    #
    #     self.assertContains(filter_response, "Task1")
    #     self.assertNotContains(filter_response, "Task2")


class TaskCreateTest(MessagesTestMixin, TestCase):
    """Test task creation."""

    fixtures = ["test_users", "test_status", "test_tasks"]
    exists_error: str = "Task with this Name already exists."

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.response = self.client.get(
            reverse_lazy("create_task")
        )

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "form.html")

    def test_create_view_contains_correct_fields(self):
        self.assertContains(self.response, "Create task")
        self.assertContains(self.response, "Name")
        self.assertContains(self.response, "Description")
        self.assertContains(self.response, "Status")
        self.assertContains(self.response, "Performer")
        self.assertContains(self.response, "Create")

    def test_successful_creation_of_task(self):

        count_before = Task.objects.count()

        response = self.client.post(
            path=reverse_lazy("create_task"),
            data={
                "name": "TestTask",
                "description": "Some text.",
                "status": Status.objects.first().id,
                "performer": User.objects.last().id,
            },
            follow=True,
        )
        self.assertRedirects(response, reverse_lazy("list_task"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=TaskCreateView.success_message, level=SUCCESS)
            ]
        )

        count_after = Task.objects.count()

        self.assertFalse(count_after == count_before)
        self.assertEqual("TestTask", Task.objects.last().name)
