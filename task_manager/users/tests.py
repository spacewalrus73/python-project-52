from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.messages.test import MessagesTestMixin

from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm


class CreateUserTest(MessagesTestMixin ,TestCase):
    """Test create user."""
    def setUp(self):
        self.view_response = self.client.get(reverse_lazy("create_user"))
        self.form = UserRegistrationForm


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
# TODO Check forms erros
