from collections.abc import Iterable
from json import load
from typing import Any

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import ERROR
from django.contrib.messages import INFO
from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.core.permission_mixins import UserLoginRequiredMixin
from task_manager.core.views import UserLoginView
from task_manager.users.models import User

LinkNames: Iterable[str, ...] = tuple


class AuthTestCase(MessagesTestMixin, TestCase):
    """Testcase special for auth system and homepage."""

    credentials: dict = {
        "username": "user",
        "password": "123",
    }

    invalid_credentials: dict = {
        "username": "UsEr",
        "password": "12$",
    }

    # Text to check from homepage
    home_page_text: LinkNames = (
        _("Practical programming courses"),
        _("Hello from Hexlet!"),
        _("Hexlet"), _("Learn more"),
    )

    # Persistently displayed link names, regardless of authorisation
    permanent_link_names: LinkNames = (_("Task manager"), _("Users"))

    # Link names displayed on an unauthorised homepage
    not_auth_fields: LinkNames = permanent_link_names \
        + (_("Enter"), _("Registration")) \
        + home_page_text

    # Link names displayed on authorised homepage
    auth_fields: Iterable = permanent_link_names \
        + (_("Statuses"), _("Labels"), _("Tasks"), _("Log out")) \
        + home_page_text

    # Permanent link, which should always contains on html page
    permanent_links: LinkNames = ("/", "/users/", "https://ru.hexlet.io/")

    # Links to pages on not authorised homepage
    not_auth_links: LinkNames = permanent_links \
        + ("/login/", "/users/create/")
    # Links to pages on authorised homepage
    auth_links: LinkNames = permanent_links \
        + ("/statuses/", "/labels/", "/tasks/", "/logout/")

    login_error_message: str = AuthenticationForm \
        .error_messages \
        .get("invalid_login") % {"username": "username"}

    login_denied_message: Message = Message(
        message=UserLoginRequiredMixin.denied_message, level=ERROR
    )

    success_login_message: Message = Message(
        message=UserLoginView.success_message, level=SUCCESS
    )

    success_logout_message: Message = Message(
        message=_("You're logged out"), level=INFO
    )

    def setUp(self) -> None:
        User.objects.create_user(**self.credentials)
        self.login_view = self.client.get(reverse_lazy("login"))
        self.home_view = self.client.get(reverse_lazy("home"))

    @staticmethod
    def serialize(file: str) -> Any:
        """Serialize from json to python."""
        with open(file) as file:
            return load(file)
