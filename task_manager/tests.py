from http import HTTPStatus

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import INFO
from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.views import UserLoginView


class HomePageTest(TestCase):
    """Simple test for homepage."""
    def setUp(self):
        self.response = self.client.get(reverse_lazy("home"))

    def test_home_page_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, template_name="home.html")

    def test_home_page_contains_correct_fields(self):
        self.assertContains(self.response, "Task manager")
        self.assertContains(self.response, "Enter")
        self.assertContains(self.response, "Users")
        self.assertContains(self.response, "Practical programming courses")
        self.assertContains(self.response, "Learn more")
        self.assertContains(self.response, "Registration")
        self.assertContains(self.response, "Hello from Hexlet!")
        self.assertContains(self.response, "Hexlet")


class AuthSystemTest(MessagesTestMixin, TestCase):
    """Test login and logout user."""

    test_username: str = "TestUser"
    test_password: str = "123"
    error_message: str = (
            AuthenticationForm.
            error_messages.
            get("invalid_login") % {"username": "username"}
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
                "password": self.test_password,
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
        response = self.client.post(path=reverse_lazy("logout"))

        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message="You're logged out", level=INFO)
            ]
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("home"))
