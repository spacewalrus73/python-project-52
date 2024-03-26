from http import HTTPStatus

from django.contrib.messages import Message
from django.contrib.messages import SUCCESS
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.statuses.views import StatusCreateView as createView
from task_manager.statuses.views import StatusDeleteView as deleteView
from task_manager.statuses.views import StatusUpdateView as updateView
from task_manager.users.models import User


class IndexStatusTest(MessagesTestMixin, TestCase):
    """Test statuses list."""

    fixtures = ["test_users"]

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.response = self.client.get(reverse_lazy("list_status"))

    def test_list_view_returns_correct_response(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "list_objects.html")

    def test_list_view_contains_correct_fields(self):
        self.assertContains(self.response, "name")
        self.assertContains(self.response, "ID")
        self.assertContains(self.response, "Creation date")
        self.assertContains(self.response, "Create status")
        self.assertContains(self.response, "Statuses")


class CreateStatusTest(MessagesTestMixin, TestCase):
    """Test create status."""

    fixtures = ["test_users", "test_status"]
    exists_error: str = "Status with this Name already exists."

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            reverse_lazy("create_status")
        )

    def test_create_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "form.html")

    def test_create_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Create status")
        self.assertContains(self.view_response, "Create")
        self.assertContains(self.view_response, "Name")

    def test_successful_creation_of_status(self):

        count_before = Status.objects.count()

        response = self.client.post(
            path=reverse_lazy("create_status"),
            data={"name": "NewStatus"}
        )

        self.assertRedirects(response, reverse_lazy("list_status"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=createView.success_message, level=SUCCESS)
            ]
        )

        count_after = Status.objects.count()

        self.assertFalse(count_before == count_after)
        self.assertEqual("NewStatus", Status.objects.last().name)

    def test_create_already_exists_status_name(self):
        response = self.client.post(
            path=reverse_lazy("create_status"),
            data={"name": "TestStatus"}
        )

        self.assertContains(response, self.exists_error)


class UpdateStatusTest(MessagesTestMixin, TestCase):
    """Test update status."""

    fixtures = ["test_users", "test_status"]

    exists_error: str = "Status with this Name already exists."

    def setUp(self):
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            reverse_lazy(
                viewname="update_status",
                kwargs={"pk": Status.objects.first().id}
            )
        )

    def test_update_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "form.html")

    def test_update_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "name")
        self.assertContains(self.view_response, "Change of status")
        self.assertContains(self.view_response, "Change")

    def test_successful_update_status(self):
        exist_status = Status.objects.first()
        count_before = Status.objects.count()
        response = self.client.post(
            path=reverse_lazy(
                viewname="update_status",
                kwargs={"pk": exist_status.id}
            ),
            data={"name": "NewStatusName"},
            follow=True,
        )
        count_after = Status.objects.count()

        self.assertRedirects(response, reverse_lazy("list_status"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=updateView.success_message, level=SUCCESS)
            ]
        )
        self.assertContains(response, "NewStatusName")
        self.assertNotEqual(exist_status.name, Status.objects.first().name)
        self.assertTrue(count_after == count_before)

    def test_update_status_with_exists_name(self):
        exist_status = Status.objects.first()

        response = self.client.post(
            path=reverse_lazy(
                viewname="update_status",
                kwargs={"pk": exist_status.id}
            ),
            data={"name": "SecondStatus"},
            follow=True,
        )

        self.assertContains(response, self.exists_error)


class DeleteStatusTest(MessagesTestMixin, TestCase):
    """Test delete status."""

    fixtures = ["test_users", "test_status"]

    def setUp(self):
        self.test_status_id: int = Status.objects.first().id
        self.test_status: Status = Status.objects.first()
        self.test_user: User = User.objects.first()
        self.client.force_login(self.test_user)
        self.view_response = self.client.get(
            path=reverse_lazy(
                viewname="delete_status",
                kwargs={"pk": self.test_status_id}
            ),
            follow=True,
        )

    def test_delete_view_returns_correct_response(self):
        self.assertEqual(self.view_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.view_response, "delete.html")

    def test_delete_view_contains_correct_fields(self):
        self.assertContains(self.view_response, "Status deletion")
        self.assertContains(self.view_response, f"{self.test_status.name}")
        self.assertContains(self.view_response, "Yes, delete")

    def test_successful_delete_status(self):
        response = self.client.post(
            path=reverse_lazy(
                viewname="delete_status",
                kwargs={"pk": self.test_status_id}
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy("list_status"))
        self.assertMessages(
            response=response,
            expected_messages=[
                Message(message=deleteView.success_message, level=SUCCESS)
            ]
        )
        self.assertNotContains(response, self.test_status.name)
