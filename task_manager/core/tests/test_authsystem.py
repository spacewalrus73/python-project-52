from .core_test_case import AuthTestCase


class TestAuthSystem(AuthTestCase):
    """Testing login and logout users."""

    def test_login_page_returns_correct_response(self):
        """Test code and template name"""
        self.assertEqual(self.login_view.status_code, self.OK)
        self.assertTemplateUsed(self.login_view, "form.html")

    def test_login_page_contains_correct_fields_and_tags(self):
        """Test that forms has essentials tags"""
        self.assertContains(self.login_view, "csrfmiddlewaretoken")
        self.assertContains(self.login_view, "<form")
        self.assertContains(self.login_view, "username")
        self.assertContains(self.login_view, "password")
