from http import HTTPStatus
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

from task_manager.permission_mixins import UserLoginRequiredMixin
from task_manager.users.models import User
from task_manager.views import UserLoginView


def serialize(file: str) -> Any:
    """Serialize from json to python."""
    with open(file) as file:
        return load(file)


class HomePageTest(TestCase):
    """
    Simple test for homepage.
    It available without authorization, so we test it separately.
    """
    def setUp(self):
        self.response = self.client.get(reverse_lazy("home"))

    def test_home_page_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "home.html")

    def test_home_page_contains_correct_fields(self):
        self.assertContains(self.response, "Task manager")
        self.assertContains(self.response, "Enter")
        self.assertContains(self.response, "Users")
        self.assertContains(self.response, "Practical programming courses")
        self.assertContains(self.response, "Learn more")
        self.assertContains(self.response, "Registration")
        self.assertContains(self.response, "Hello from Hexlet!")
        self.assertContains(self.response, "Hexlet")

    def tearDown(self):
        """
        Django automatically clears db after each test.
        So it is not necessary to use this method.
        """


class AuthSystemTest(MessagesTestMixin, TestCase):
    """Test login and logout user."""

    test_username: str = "TestUser"
    test_password: str = "123"
    error_message: str = (
            AuthenticationForm.
            error_messages.
            get("invalid_login") % {"username": "username"}
    )
    login_denied_message: Message = Message(
        message=UserLoginRequiredMixin.denied_message, level=ERROR
    )
    unavailable_pages: dict = serialize(
        "task_manager/fixtures/redirect_routes.json"
    )

    def setUp(self):
        self.get_response = self.client.get(reverse_lazy("login"))

    def test_login_page_returns_correct_response(self):
        self.assertTemplateUsed(self.get_response, "form.html")
        self.assertEqual(self.get_response.status_code, HTTPStatus.OK)

    def test_login_page_contains_correct_fields_and_tags(self):
        self.assertContains(self.get_response, "csrfmiddlewaretoken")
        self.assertContains(self.get_response, "Task manager")
        self.assertContains(self.get_response, "Users")
        self.assertContains(self.get_response, "Enter")
        self.assertContains(self.get_response, "Registration")
        self.assertContains(self.get_response, "username")
        self.assertContains(self.get_response, "password")
        self.assertContains(self.get_response, "Log in")
        self.assertContains(self.get_response, "Hexlet")
        self.assertContains(self.get_response, "<form")

    def test_valid_login_user(self):
        # Pass the user through Django Authentication system
        # That means register him for the first time
        User.objects.create_user(
            username=self.test_username,
            password=self.test_password,
        )
        # Create response by passing user data
        response = self.client.post(
            path=reverse_lazy("login"),
            data={
                "username": self.test_username,
                "password": self.test_password
            },
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("home"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=UserLoginView.success_message, level=SUCCESS)
            ]
        )
        # These fields are only available after login
        self.assertContains(response, "Users")
        self.assertContains(response, "Statuses")
        self.assertContains(response, "Tags")
        self.assertContains(response, "Tasks")
        self.assertContains(response, "Log out")

    def test_invalid_login_user(self):
        # create response with invalid login
        response = self.client.post(
            path=reverse_lazy("login"),
            data={
                "username": self.test_username + "s",
                "password": self.test_password
            },
            follow=True,
        )

        self.assertContains(response, self.error_message)
        # If login failed, response must not contain these links
        self.assertNotContains(response, "Statuses")
        self.assertNotContains(response, "Tags")
        self.assertNotContains(response, "Tasks")
        self.assertNotContains(response, "Log out")

    def test_logout_user(self):
        """
        Logout don't render template.
        It just logs out and redirects to homepage.
        """
        response = self.client.post(reverse_lazy("logout"))

        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message="You're logged out", level=INFO)
            ]
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("home"))

    def test_unauthorized_user_cannot_access_some_pages(self):
        """
        Test the behaviour when an unauthorized user tries
         to access pages, he shouldn't able to access.
        """
        for expected_url, response_url in self.unavailable_pages.items():
            if isinstance(response_url, str):
                response = self.client.get(
                    path=reverse_lazy(response_url),
                    follow=True
                )
            else:
                response = self.client.get(
                    path=reverse_lazy(
                        viewname=response_url[0],
                        kwargs={"pk": response_url[1]}
                    ),
                    follow=True
                )
            self.assertRedirects(response, expected_url)
            self.assertMessages(response, [self.login_denied_message])
