from http import HTTPStatus

from django.contrib.messages.test import MessagesTestMixin
from django.urls import reverse_lazy

from .core_test_case import AuthTestCase


class TestAuthSystem(MessagesTestMixin, AuthTestCase):
    """Testing login and logout users."""

    def test_login_page_returns_correct_response(self):
        """Test code and template name"""
        self.assertEqual(self.login_view.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.login_view, "form.html")

    def test_login_page_contains_correct_fields_and_tags(self):
        """Test that forms has essentials tags"""
        self.assertContains(self.login_view, "csrfmiddlewaretoken")
        self.assertContains(self.login_view, "<form")
        self.assertContains(self.login_view, "username")
        self.assertContains(self.login_view, "password")

    def test_valid_login_user(self):
        """Test valid user log in"""
        logged_response = self.client.post(
            path=reverse_lazy("login"),
            data=self.credentials,
            follow=True,
        )
        self.assertRedirects(logged_response, reverse_lazy("home"))
        self.assertMessages(
            response=logged_response,
            expected_messages=[self.success_login_message]
        )

    def test_invalid_login_user(self):
        """Test invalid login and check errors message"""
        invalid_response = self.client.post(
            path=reverse_lazy("login"),
            data=self.invalid_credentials,
            follow=True,
        )
        self.assertContains(invalid_response, self.login_error_message)

    def test_logout_user(self):
        """Test redirects to homepage, logout don't render template."""
        self.client.post(
            path=reverse_lazy("login"),
            data=self.credentials,
            follow=True,
        )
        logout_response = self.client.post(reverse_lazy("logout"))
        self.assertMessages(
            response=logout_response,
            expected_messages=[self.success_logout_message]
        )
        self.assertEqual(logout_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(logout_response, reverse_lazy("home"))

    def test_unauthorised_user_cannot_access_some_pages(self):
        """
        Test the behavior when an unauthorised user tries to access
        pages, he shouldn't able to access.
        """
        unavailable_pages: dict = AuthTestCase.serialize(
            "task_manager/fixtures/redirect_routes.json"
        )
        for expected_url, response_url in unavailable_pages.items():
            if isinstance(response_url, str):
                response = self.client.get(
                    path=reverse_lazy(response_url),
                    follow=True,
                )
            else:
                response = self.client.get(
                    path=reverse_lazy(
                        viewname=response_url[0],
                        kwargs={"pk": response_url[1]},
                    ),
                    follow=True,
                )
            self.assertRedirects(response, expected_url)
            self.assertMessages(response, [self.login_denied_message])
