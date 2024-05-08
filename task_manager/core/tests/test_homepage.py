from http import HTTPStatus

from django.urls import reverse_lazy

from .core_test_case import AuthTestCase


class TestHomePage(AuthTestCase):
    """Simple tests for homepage. It available without authorization."""

    def test_home_page_returns_correct_response(self):
        """Test code and template name"""
        self.assertEqual(self.home_view.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.home_view, "home.html")

    def test_home_page_contains_correct_fields_without_authorization(self):
        """
        Test that fields name and their links
        are displayed for not auth user
        """
        for test_field_name in self.not_auth_fields:
            self.assertContains(self.home_view, test_field_name)
        for test_link in self.not_auth_links:
            self.assertContains(self.home_view, test_link)

    def test_home_page_contains_correct_fields_with_authorization(self):
        """
        Test that fields name and their links
        are displayed for auth user
        """
        logged_response = self.client.post(
            path=reverse_lazy("login"),
            data=self.credentials,
            follow=True,
        )
        for test_field_name in self.auth_fields:
            self.assertContains(logged_response, test_field_name)
        for test_link in self.auth_links:
            self.assertContains(logged_response, test_link)
