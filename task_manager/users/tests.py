from http import HTTPStatus

from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import User


class CreateUserTest(MessagesTestMixin, TestCase):
    """Test create user."""
    def setUp(self):
        self.view_response = self.client.get(reverse_lazy("create_user"))
        self.form = UserRegistrationForm
        self.test_name = "TestUser"
        self.test_passwd = "000"
        self.users_count = User.objects.count()

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, 'form.html')

    def test_create_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Registration")
        self.assertContains(self.view_response, "first_name")
        self.assertContains(self.view_response, "last_name")
        self.assertContains(self.view_response, "username")
        self.assertContains(self.view_response, "password1")
        self.assertContains(self.view_response, "password2")
        self.assertContains(self.view_response, "Register")

    def test_valid_registration_user(self):
        response = self.client.post(
            path=reverse_lazy("create_user"),
            data={
                "first_name": self.test_name,
                "last_name": self.test_name,
                "username": self.test_name,
                "password1": self.test_passwd,
                "password2": self.test_passwd,

            },
            follow=True
        )

        self.assertRedirects(response, reverse_lazy("login"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(
                    level=SUCCESS, message="User is successfully registered"
                )
            ]
        )
        # Check that user was created in db
        self.assertNotEqual(self.users_count, User.objects.count())
        # Check that user can log in now
        self.client.post(
            path=reverse_lazy("login"),
            data={
                "username": self.test_name,
                "password": self.test_passwd,
            }
        )
