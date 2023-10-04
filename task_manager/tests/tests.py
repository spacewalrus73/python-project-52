from django.test import TestCase


class TestMainApp(TestCase):

    fixtures = ['test_users.json']

    def test_details_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello from Hexlet!", response.content)
        self.assertIn(b"Task manager", response.content)
        self.assertIn(b"Users", response.content)
        self.assertIn(b"Enter", response.content)
        self.assertIn(b"Registration", response.content)

    def test_login_logout(self):
        auth = self.client.login(username='PaulMCc', password='superPaul333')
        person = self.client.get(pk=1)
        print(person.username)
        self.assertTrue(auth)
        response = self.client.get('/')
        self.assertIn(b"Statuses", response.content)
        self.assertIn(b"Tags", response.content)
        self.assertIn(b"Tasks", response.content)
        self.assertIn(b"Log out", response.content)
        auth = self.client.logout()
        self.assertFalse(auth)
