from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from task_manager.core.permission_mixins import TaskDeletionTestMixin
from task_manager.core.permission_mixins import UserLoginRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskIndexView(UserLoginRequiredMixin, FilterView, ListView):
    """List all tasks. Authorization required."""
    model = Task
    template_name = "list_objects.html"
    filterset_class = TaskFilter
    extra_context = {
        "title": _("Tasks"),
        "button_text": _("Create task"),
        "filter_text": _("Show"),
        "captions": [
            _("Name"), _("Status"), _("Author"),
            _("Performer"), _("Creation date"),
        ],
        "url_to_create": reverse_lazy("create_task"),
        "url_to_update": "update_task",
        "url_to_delete": "delete_task",
    }


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    """Show task info page."""
    model = Task
    template_name = "task_detail.html"


class TaskCreateView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """The view shows create from for new task. Authorization required."""
    # CreateView attrs
    model = Task
    template_name = "form.html"
    form_class = TaskForm

    extra_context = {
        "title": _("Create task"),
        "button_text": _("Create"),
        "needs_messages": True,
    }
    success_url = reverse_lazy("list_task")
    # SuccessMessageMixin attrs
    success_message = _("Task successfully created")

    def form_valid(self, form):
        """Add authorized user as an author."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Tasks update view."""

    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy("list_task")
    extra_context = {
        "title": _("Task modification"),
        "button_text": "Change",
        "needs_messages": False,
    }
    # SuccessMessageMixin
    success_message = _("Task successfully changed")


class TaskDeleteView(UserLoginRequiredMixin,
                     TaskDeletionTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("list_task")
    extra_context = {
        "title": _("Task deletion"),
        "url_for_delete": "delete_task",
    }
    # SuccessMessageMixin attrs
    success_message = _("Task successfully deleted")
