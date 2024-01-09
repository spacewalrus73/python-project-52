from django.test import Client
from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import User
from django.contrib.auth.forms import AuthenticationForm


class IndexPageTest(TestCase):

    def test_index_page_returns_correct_response(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "Hello from Hexlet!")


class LogInPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.form = AuthenticationForm
        self.response = self.client.get(reverse('login'))
        # Pass the user through the Django Authentication system
        self.auth_user = User.objects.create_user(
            username="TestUser",
            password="123",
        )

    def test_login_page_returns_correct_response(self):
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertEqual(self.response.status_code, 200)

    def test_form_has_valid_fields(self):
        self.assertTrue(issubclass(self.form, AuthenticationForm))
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        self.assertContains(self.response, "username")
        self.assertContains(self.response, "Log in")
        self.assertContains(self.response, "password")

    def test_login_page_form_rendering(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_login_logout_exists_user(self):
        # Test user exist
        self.assertEqual(User.objects.count(), 1)
        # Check password for user
        self.assertTrue(self.auth_user.check_password("123"))
        # Make the right authentication
        response_in = self.client.post(
            reverse('login'),
            {
                "username": "TestUser",
                "password": "123",
            },
            follow=True
        )
        self.assertRedirects(response_in, reverse('index'))
        self.assertContains(response_in, "You're logged in")
        self.assertContains(response_in, "Statuses")
        self.assertContains(response_in, "Tasks")
        self.assertContains(response_in, "Tags")
        # Make logout
        logout_response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(logout_response, reverse('login'))
        self.assertEqual(logout_response.status_code, 200)
        self.assertContains(logout_response, "Log in")


