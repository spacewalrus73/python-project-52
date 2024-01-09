from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm, UserUpdateForm


class RegistrationPageTest(TestCase):

    def setUp(self):
        self.form = UserRegistrationForm
        self.response = self.client.get(reverse('create_user'))

    def test_registration_page_returns_correct_response(self):
        self.assertTemplateUsed(self.response, 'users/registration.html')
        self.assertEqual(self.response.status_code, 200)

    def test_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, UserRegistrationForm))
        self.assertTrue("username" in self.form.Meta.fields)
        self.assertTrue("first_name" in self.form.Meta.fields)
        self.assertTrue("last_name" in self.form.Meta.fields)
        self.assertContains(self.response, "Registration")
        self.assertContains(self.response, "password1")
        self.assertContains(self.response, "password2")
        # Test valid form
        test_form = self.form({
            "username": "Username",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "password1": "Test_pass",
            "password2": "Test_pass",
        })
        self.assertTrue(test_form.is_valid())
        # Test invalid form
        test_form = self.form({
            "username": "",
            "first_name": "",
            "last_name": "",
            "password1": "",
            "password2": "",
        })
        self.assertFalse(test_form.is_valid())

    def test_registration_page_form_rendering(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        # Test invalid form
        response_with_error = self.client.post(
            reverse('create_user'),
            {
                "username": "",
                "first_name": "",
                "last_name": "",
                "password1": "",
                "password2": "",
            }
        )
        self.assertContains(response_with_error, 'This field is required')
        # Test valid form redirect to login page
        valid_response = self.client.post(
            reverse('create_user'),
            {
                "username": "username",
                "first_name": "name1",
                "last_name": "name2",
                "password1": "pass",
                "password2": "pass",
            }
        )
        self.assertRedirects(valid_response, reverse('login'))
        self.assertEqual(User.objects.count(), 1)
        # Test list users page has created user
        response_index = self.client.get(reverse('list_user'))

        self.assertTemplateUsed(response_index, 'users/index.html')
        self.assertEqual(response_index.status_code, 200)
        self.assertContains(response_index, "username")


class UpdatingPageTest(TestCase):

    fixtures = ['test_user']

    def setUp(self):
        self.form = UserUpdateForm
        self.user = User.objects.get(id=1)
        self.response = self.client.get(
            reverse('update_user',
                    args=[self.user.id]))

    def test_update_page_returns_correct_response(self):
        # TODO Исправить: не видит темплейт
        self.assertTemplateUsed(self.response, 'users/updating.html')
        self.assertEqual(self.response.status_code, 200)

    def test_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, UserUpdateForm))
        self.assertTrue("username" in self.form.Meta.fields)
        self.assertTrue("first_name" in self.form.Meta.fields)
        self.assertTrue("last_name" in self.form.Meta.fields)
        self.assertContains(self.response, "Update user")
        self.assertContains(self.response, "password1")
        self.assertContains(self.response, "password2")

        test_form = self.form({
            "username": "TheUser",
            "password1": "000",
            "password2": "000"
        }, instance=self.user)

        self.assertTrue(test_form.is_valid())

        test_form.save()

        self.assertEqual(self.user.username, "TheUser")
        self.assertEqual(User.objects.count(), 1)

    def test_form_can_be_invalid(self):

        test_form = self.form({
            "username": "",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "password1": "Test_pass",
            "password2": "Test_pass",
        }, instance=self.user)

        self.assertFalse(test_form.is_valid())

    def test_update_page_form_rendering(self):
        # TODO Скорее всего происходит редирект, т.к. нет прав на изменение у не авторизованного user.
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        # Test invalid form
        response_with_error = self.client.post(
            reverse('create_user'),
            {
                "username": "",
                "first_name": "",
                "last_name": "",
                "password1": "",
                "password2": "",
            },
            instance=self.user
        )
        self.assertContains(response_with_error, 'This field is required')
        # Test valid form
        response_valid = self.client.post(
            reverse('update_user', args=[self.user.id]),
            {
                "username": "User111",
                "password1": "111",
                "password2": "111",
            },
            instance=self.user
        )

        self.assertRedirects(response_valid, expected_url=reverse('list_user'))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'User111')


class DeletionPageTest(TestCase):

    fixtures = ['test_user']

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_delete_page_has_user_fullname_and_cautions(self):
        # Test user already exists by fixture
        self.assertEqual(User.objects.count(), 1)
        # Make response with delete
        del_response = self.client.get(
            reverse('delete_user', args=[self.user.id]))
        self.assertContains(del_response, self.user.get_full_name())
        self.assertContains(del_response, "Are you sure, you want to delete?")
        self.assertContains(del_response, "Yes, delete")

    def test_delete_page_deletes_user(self):
        # Test user already exists by fixture
        self.assertEqual(User.objects.count(), 1)
        # Make response with deletion
        self.client.post(reverse('delete_user', args=[self.user.id]))
        # Make sure that user was deleted
        self.assertEqual(User.objects.count(), 0)