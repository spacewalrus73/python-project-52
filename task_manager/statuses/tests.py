from http import HTTPStatus

from django.contrib.messages import ERROR
from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.permission_mixins import UserLoginRequiredMixin as loginMixin
from task_manager.statuses.models import Status
from task_manager.statuses.views import StatusCreateView as createView
from task_manager.users.models import User


class CreateStatusTest(MessagesTestMixin, TestCase):
    """Test create status."""

    fixtures = ["test_users", "test_status"]

    def setUp(self):
        self.test_user = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(reverse_lazy("create_status"))

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "form.html")

    def test_create_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Create status")
        self.assertContains(self.view_response, "Create")
        self.assertContains(self.view_response, "Name")

    def test_not_auth_user_cant_create_status(self):
        # imitate anonymous user
        self.test_user.is_active = False
        self.test_user.save()

        login_response = self.client.get(reverse_lazy("create_status"))

        self.assertRedirects(login_response, "/login/?next=/statuses/create/")
        self.assertMessages(
            response=login_response,
            expected_messages=[
                Message(message=loginMixin.denied_message, level=ERROR)
            ]
        )

    def test_successful_creation_of_status(self):
        response = self.client.post(
            path=reverse_lazy("create_status"),
            data={"name": "NewStatus"}
        )

        self.assertRedirects(response, reverse_lazy("list_status"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=createView.success_message, level=SUCCESS)
            ]
        )

        count_after = Status.objects.count()

        self.assertTrue(2 == count_after)
        self.assertEqual("NewStatus", Status.objects.last().name)

    def test_create_already_exists_status_name(self):
        response = self.client.post(
            path=reverse_lazy("create_status"),
            data={"name": "TestStatus"}
        )

        self.assertContains(response, "Status with this Name already exists.")
