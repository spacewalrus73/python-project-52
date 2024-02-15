from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from task_manager.permission_mixins import UserLoginRequiredMixin
from task_manager.tasks.forms import TaskFilterForm
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskIndexView(UserLoginRequiredMixin,
                    FilterView,
                    ListView):
    """List all tasks. Authorization required."""
    model = Task
    template_name = "tasks_table.html"
    context_object_name = "tasks"
    filterset_class = TaskFilterForm
    extra_context = {
        "button_text": _("Show")
    }


class TaskCreateView(UserLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
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
        """Add authorized user as author."""
        form.instance.author = self.request.user
        return super().form_valid(form)
