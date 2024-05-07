from collections.abc import Iterable
from http import HTTPStatus
from json import load
from typing import Any

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import ERROR
from django.contrib.messages import Message
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.core.permission_mixins import UserLoginRequiredMixin
from task_manager.users.models import User


TEXT_PAGE = (
    "Practical programming courses",
    "Hello from Hexlet!",
    "Hexlet", "Learn more"
)


class AuthTestCase(TestCase):
    """Testcase special for auth system and homepage."""

    credentials: dict = {
        "username": "user",
        "password": "123",
    }

    OK = HTTPStatus.OK

    not_auth_fields: Iterable = (
        "Task manager", "Users", "Enter", "Registration",
        *TEXT_PAGE
    )

    auth_fields: Iterable = (
        "Task manager", "Users", "Statuses", "Labels", "Tasks", "Log out",
        *TEXT_PAGE
    )

    not_auth_links: Iterable = ("/users/", "/login/")

    auth_links: Iterable = (
        "/users/", "/logout/", "/statuses/", "/labels/", "/tasks/"
    )

    error_message: str = AuthenticationForm \
        .error_messages \
        .get("invalid_login") % {"username": "username"}

    login_denied_message: Message = Message(
        message=UserLoginRequiredMixin.denied_message, level=ERROR
    )

    def setUp(self) -> None:
        self.user = User.objects.create_user(**self.credentials)
        self.login_view = self.client.get(reverse_lazy("login"))
        self.home_view = self.client.get(reverse_lazy("home"))
        self.logged = self.client.post(
            path=reverse_lazy("login"),
            data=self.credentials,
            follow=True,
        )

    @staticmethod
    def serialize(file: str) -> Any:
        """Serialize from json to python."""
        with open(file) as file:
            return load(file)
