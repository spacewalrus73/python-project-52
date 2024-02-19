from http import HTTPStatus

from django.contrib.messages import ERROR
from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.permission_mixins import UserLoginRequiredMixin as loginMixin
from task_manager.users.models import User


class TaskIndexTest(MessagesTestMixin, TestCase):
    """Test tasks list. Authentication required."""

    fixtures: list = ["test_users", "test_status", "test_tasks"]
    list_task: str = reverse_lazy("list_task")

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(self.list_task)

    def not_auth_user_cant_reach_task_list_page(self):
        # imitate anonymous user
        self.test_user.is_active = False
        self.test_user.save()

        view_response = self.client.get(self.list_task)

        self.assertRedirects(view_response, "/login/?next=/tasks/")
        self.assertMessages(
            response=view_response,
            expected_messages=[
                Message(message=loginMixin.denied_message, level=ERROR)
            ]
        )

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

    # How to test filter????????????
    # def test_filter_form(self):
    #     filtered = self.client.get(
    #         path=self.list_task,
    #         data={
    #             "Status": "SecondStatus",
    #             "Performer": "Linus Torvalds"
    #         }
    #     )
    #     self.assertNotContains(filtered, "TestStatus")
