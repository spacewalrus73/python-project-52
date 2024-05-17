from http import HTTPStatus

from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.tests.users_test_case import UsersTestCase


class TestCreateUser(UsersTestCase):
    """Test create users"""

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.create_view.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.create_view, "form.html")

    def test_create_view_contains_correct_fields(self):
        for field_name in self.create_view_fields:
            self.assertContains(self.create_view, field_name)

    def test_valid_registration(self):
        before_users_count = User.objects.count()
        create_user_response = self.client.post(
            path=reverse_lazy("create_user"),
            data={
                "first_name": self.test_username,
                "last_name": self.test_username,
                "username": self.test_username,
                "password1": self.test_password,
                "password2": self.test_password,
            },
            follow=True,
        )
        self.assertRedirects(create_user_response, reverse_lazy("login"))
        self.assertMessages(
            response=create_user_response,
            expected_messages=[self.success_created_message]
        )
        self.assertNotEqual(before_users_count, User.objects.count())

    def test_invalid_user_registration_with_unique_username(self):
        exists_user = User.objects.first()
        invalid_response = self.client.post(
            path=reverse_lazy("create_user"),
            data={
                "first_name": exists_user.first_name,
                "last_name": exists_user.last_name,
                "username": exists_user.username,
                "password1": exists_user.password,
                "password2": exists_user.password,
            },
            follow=True,
        )
        self.assertContains(invalid_response, self.unique_username)
