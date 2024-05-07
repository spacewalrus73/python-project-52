from .core_test_case import AuthTestCase


class TestHomePage(AuthTestCase):
    """Simple tests for homepage. It available without authorization."""

    def test_home_page_returns_correct_response(self):
        """Test code and template name"""
        self.assertEqual(self.home_view.status_code, self.OK)
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
        for test_field_name in self.auth_fields:
            self.assertContains(self.logged, test_field_name)
        for test_link in self.auth_links:
            self.assertContains(self.logged, test_link)
