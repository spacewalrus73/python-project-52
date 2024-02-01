from http import HTTPStatus

from django.contrib.messages import ERROR
from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.permission_mixins import UserLoginRequiredMixin
from task_manager.permission_mixins import UserPermissionTestMixin
from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import User
from task_manager.users.views import UserUpdateView


class CreateUserTest(MessagesTestMixin, TestCase):
    """Test create user."""

    fixtures = ["test_users"]

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
        login_response = self.client.post(
            path=reverse_lazy("login"),
            data={
                "username": self.test_name,
                "password": self.test_passwd,
            },
            follow=True,
        )
        self.assertMessages(
            response=login_response,
            expected_messages=[
                Message(
                    message="You're logged in",
                    level=SUCCESS,
                )
            ]
        )

    def test_invalid_user_registration_with_password_mismatch(self):
        response = self.client.post(
            path=reverse_lazy("create_user"),
            data={
                "first_name": self.test_name,
                "last_name": self.test_name,
                "username": self.test_name,
                "password1": self.test_passwd,
                # Make different second password
                "password2": self.test_passwd + "0",

            },
            follow=True
        )
        err_message = self.form.error_messages.get("password_mismatch")

        self.assertContains(response, err_message)

    def test_invalid_user_registration_with_unique_username(self):
        # Check that fixture was loaded
        exists_user = User.objects.get(username="PythonLover")

        self.assertEqual(exists_user.username, "PythonLover")

        # Try to registrate user with exists username
        response = self.client.post(
            path=reverse_lazy("create_user"),
            data={
                "first_name": self.test_name,
                "last_name": self.test_name,
                "username": exists_user.username,
                "password1": self.test_passwd,
                "password2": self.test_passwd,

            }
        )
        self.assertContains(
            response=response,
            text="A user with that username already exists."
        )


class UpdateUserTest(MessagesTestMixin, TestCase):
    """Test update user."""

    fixtures = ["test_users"]

    def setUp(self):
        self.test_user = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            reverse_lazy("update_user", kwargs={"pk": self.test_user.id})
        )
        self.success_message_update = UserUpdateView.success_message
        self.login_err_message = UserLoginRequiredMixin.denied_message
        self.rights_err = UserPermissionTestMixin.permission_denied_message

    def test_update_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "form.html")

    def test_update_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Update user")
        self.assertContains(self.view_response, "first_name")
        self.assertContains(self.view_response, "last_name")
        self.assertContains(self.view_response, "username")
        self.assertContains(self.view_response, "password1")
        self.assertContains(self.view_response, "password2")
        self.assertContains(self.view_response, "Update")

    def test_permission_not_auth_user_cant_change_staff(self):
        """Not auth user can't change any other users or himself."""
        # imitate anonymous user
        self.test_user.is_active = False
        self.test_user.save()

        response = self.client.get(
            path=reverse_lazy("update_user", kwargs={"pk": self.test_user.id}),
            follow=True,
        )

        self.assertRedirects(
            response=response,
            expected_url="/login/?next=/users/1/update/",
        )
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=self.login_err_message, level=ERROR)
            ]
        )

    def test_permission_user_cant_change_not_him_staff(self):
        # 2 - id of second test_user,
        # that could potentially be modified by active user
        response = self.client.get(
            path=reverse_lazy("update_user", kwargs={"pk": 2}),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[Message(message=self.rights_err, level=ERROR)]
        )

    def test_successful_update_user(self):
        new_data = {
                "first_name": "NewFirstName",
                "last_name": "NewLastName",
                "username": "NewUserName",
                "password1": "NewPasswd",
                "password2": "NewPasswd",
            }

        response = self.client.post(
            path=reverse_lazy("update_user", kwargs={"pk": self.test_user.id}),
            data=new_data,
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=self.success_message_update, level=SUCCESS)
            ]
        )

        updated_test_user = User.objects.get(username=new_data.get("username"))

        self.assertEqual(
            updated_test_user.first_name,
            new_data.get("first_name")
        )
        self.assertEqual(
            updated_test_user.last_name,
            new_data.get("last_name")
        )
        self.assertEqual(
            updated_test_user.username,
            new_data.get("username")
        )


class DeleteUserTest(MessagesTestMixin, TestCase):
    """Test delete user."""
