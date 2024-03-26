from http import HTTPStatus

from django.contrib.messages import ERROR
from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.permission_mixins import UserPermissionTestMixin
from task_manager.users.forms import UserRegistrationForm
from task_manager.users.models import User
from task_manager.users.views import UserCreateView
from task_manager.users.views import UserDeleteView
from task_manager.users.views import UserUpdateView
from task_manager.views import UserLoginView


class CreateUserTest(MessagesTestMixin, TestCase):
    """Test create user."""

    fixtures = ["test_users"]

    passwrd_mismatch: str = UserRegistrationForm.error_messages.get(
            "password_mismatch"
        )
    unique_username: str = "A user with that username already exists."
    test_name: str = "TestUser"
    test_passwd: str = "000"

    def setUp(self):
        self.view_response = self.client.get(reverse_lazy("create_user"))

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
        before_users_count = User.objects.count()
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
                Message(level=SUCCESS, message=UserCreateView.success_message)
            ]
        )
        # Check that user was created in db
        self.assertNotEqual(before_users_count, User.objects.count())
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
                Message(message=UserLoginView.success_message, level=SUCCESS)
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

        self.assertContains(response, self.passwrd_mismatch)

    def test_invalid_user_registration_with_unique_username(self):
        # Check that fixture was loaded
        exists_user = User.objects.first()

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

        self.assertContains(response, self.unique_username)


class UpdateUserTest(MessagesTestMixin, TestCase):
    """Test update user."""

    fixtures = ["test_users"]

    new_data: dict = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "username": "NewUserName",
        "password1": "NewPasswd",
        "password2": "NewPasswd",
    }

    def setUp(self):
        self.test_user = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            reverse_lazy(
                viewname="update_user",
                kwargs={"pk": self.test_user.pk}
            )
        )

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

    def test_permission_user_cant_change_not_him_staff(self):
        # 2 - id of second test_user,
        # that could potentially be modified by active user
        response = self.client.get(
            path=reverse_lazy(viewname="update_user", kwargs={"pk": 3}),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(
                    message=UserPermissionTestMixin.permission_denied_message,
                    level=ERROR
                )
            ]
        )

    def test_successful_update_user(self):
        response = self.client.post(
            path=reverse_lazy(
                viewname="update_user",
                kwargs={"pk": self.test_user.id}
            ),
            data=self.new_data,
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(
                    message=UserUpdateView.success_message,
                    level=SUCCESS
                )
            ]
        )

        updated_test_user = User.objects.get(
            username=self.new_data.get("username")
        )

        self.assertEqual(
            updated_test_user.first_name,
            self.new_data.get("first_name")
        )
        self.assertEqual(
            updated_test_user.last_name,
            self.new_data.get("last_name")
        )
        self.assertEqual(
            updated_test_user.username,
            self.new_data.get("username")
        )


class DeleteUserTest(MessagesTestMixin, TestCase):
    """Test delete user."""

    fixtures = ["test_users"]

    users_count: int = User.objects.count()

    def setUp(self):
        self.test_user = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            reverse_lazy(
                viewname="delete_user",
                kwargs={"pk": self.test_user.id}
            )
        )

    def test_delete_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "delete.html")

    def test_delete_view_contains_correct_context_values(self):
        self.assertContains(self.view_response, "User deletion")
        self.assertContains(self.view_response, "Yes, delete")
        self.assertContains(self.view_response, f"{self.test_user.first_name}")
        self.assertContains(self.view_response, f"{self.test_user.last_name}")

    def test_user_cant_delete_staff_that_dont_belong_to_him(self):
        response = self.client.post(
            path=reverse_lazy(viewname="delete_user", kwargs={"pk": 3}),
            follow=True,

        )
        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(
                    message=UserPermissionTestMixin.permission_denied_message,
                    level=ERROR
                )
            ]
        )

    def test_successfully_delete_user(self):
        response = self.client.post(
            path=reverse_lazy(
                viewname="delete_user",
                kwargs={"pk": self.test_user.id}
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_user"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(
                    message=UserDeleteView.success_message,
                    level=SUCCESS
                )
            ]
        )
        self.assertNotEqual(self.users_count, User.objects.count())
        self.assertNotContains(response, self.test_user.username)
