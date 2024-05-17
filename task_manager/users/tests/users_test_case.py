from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import UserRegistrationForm
from task_manager.users.views import UserCreateView


class UsersTestCase(MessagesTestMixin, TestCase):
    """Testcase special for test user model."""

    fixtures = ["test_users"]

    password_mismatch: str = UserRegistrationForm.error_messages.get(
        "password_missmatch"
    )
    unique_username: str = _("A user with that username already exists.")

    create_view_fields: list = [
        _("Registration"), _("Register"),
        "first_name", "last_name",
        "username", "password1", "password2"
    ]

    success_created_message: Message = Message(
        message=UserCreateView.success_message,
        level=SUCCESS,
    )

    test_username: str = "test"
    test_password: str = "123"

    def setUp(self) -> None:
        self.create_view = self.client.get(reverse_lazy("create_user"))
