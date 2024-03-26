from http import HTTPStatus

from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.labels.views import LabelCreateView as createView
from task_manager.labels.views import LabelDeleteView as deleteView
from task_manager.labels.views import LabelUpdateView as updateView
from task_manager.users.models import User


class IndexLabelTest(MessagesTestMixin, TestCase):
    """Test labels list."""

    fixtures = ["test_users"]

    def setUp(self):
        self.client.force_login(User.objects.first())
        self.response = self.client.get(reverse_lazy("list_label"))

    def test_list_view_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "list_objects.html")

    def test_list_view_contains_correct_fields(self):
        self.assertContains(self.response, "ID")
        self.assertContains(self.response, "name")
        self.assertContains(self.response, "Creation date")
        self.assertContains(self.response, "Create label")


class CreateLabelTest(MessagesTestMixin, TestCase):
    """Test create label."""

    fixtures = ["test_users", "test_labels"]
    exists_error: str = "Label with this Name already exists."

    def setUp(self):
        self.client.force_login(User.objects.first())
        self.response = self.client.get(
            reverse_lazy("create_label")
        )

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "form.html")

    def test_create_view_contains_correct_fields(self):
        self.assertContains(self.response, "Create label")
        self.assertContains(self.response, "Create")
        self.assertContains(self.response, "Name")

    def test_successful_creation_of_status(self):

        count_before = Label.objects.count()

        response = self.client.post(
            path=reverse_lazy("create_label"),
            data={"name": "FirstLabel"},
        )

        self.assertRedirects(response, reverse_lazy("list_label"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=createView.success_message, level=SUCCESS)
            ]
        )

        count_after = Label.objects.count()

        self.assertFalse(count_before == count_after)
        self.assertEqual("FirstLabel", Label.objects.last().name)

    def test_create_already_exists_label_name(self):
        response = self.client.post(
            path=reverse_lazy("create_label"),
            data={"name": "TestLabel1"}
        )
        self.assertContains(response, self.exists_error)


class UpdateLabelTest(MessagesTestMixin, TestCase):
    """Test update label."""

    fixtures = ["test_users", "test_labels"]

    exists_error: str = "Label with this Name already exists."

    def setUp(self):
        self.client.force_login(User.objects.first())
        self.view_response = self.client.get(
            reverse_lazy(
                viewname="update_label",
                kwargs={"pk": Label.objects.first().id}
            )
        )

    def test_update_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "form.html")

    def test_update_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "name")
        self.assertContains(self.view_response, "Change of label")
        self.assertContains(self.view_response, "Change")

    def test_successful_update_label(self):
        exist_label = Label.objects.first()
        count_before = Label.objects.count()
        response = self.client.post(
            path=reverse_lazy(
                viewname="update_label",
                kwargs={"pk": exist_label.id}
            ),
            data={"name": "NewTestLabelName"},
            follow=True,
        )

        count_after = Label.objects.count()

        self.assertRedirects(response, reverse_lazy("list_label"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=updateView.success_message, level=SUCCESS)
            ]
        )
        self.assertContains(response, "NewTestLabelName")
        self.assertNotEqual(exist_label.name, Label.objects.first().name)
        self.assertTrue(count_after == count_before)


class DeleteLabelTest(MessagesTestMixin, TestCase):
    """Test delete label."""

    fixtures = ["test_users", "test_labels"]

    def setUp(self):
        self.test_label_id: int = Label.objects.first().id
        self.test_label: Label = Label.objects.first()
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            path=reverse_lazy(
                viewname="delete_label",
                kwargs={"pk": self.test_label_id}
            ),
            follow=True,
        )

    def test_delete_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "delete.html")

    def test_delete_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Label deletion")
        self.assertContains(self.view_response, f"{self.test_label.name}")
        self.assertContains(self.view_response, "Yes, delete")

    def test_successful_delete_label(self):
        response = self.client.post(
            path=reverse_lazy(
                viewname="delete_label",
                kwargs={"pk": self.test_label_id}
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_label"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=deleteView.success_message, level=SUCCESS)
            ]
        )
        self.assertNotContains(response, self.test_label.name)
