import unittest
from django.test import Client


class TestMainApp(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_details_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello from Hexlet!", response.content)
        self.assertIn(b"Task manager", response.content)
        self.assertIn(b"Users", response.content)
        self.assertIn(b"Enter", response.content)
        self.assertIn(b"Registration", response.content)

    def test_login_user(self):
        auth = self.client.login(username='1234', password='123')
        self.assertTrue(auth)

