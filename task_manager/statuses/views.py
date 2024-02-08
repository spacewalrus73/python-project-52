from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from task_manager.permission_mixins import ProtectObjectDeletionMixin
from task_manager.permission_mixins import TaskManagerFormMixin
from task_manager.permission_mixins import UserLoginRequiredMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusIndexView(UserLoginRequiredMixin, ListView):
    """
    List all Status objects.
    Authorization required.
    """
    model = Status
    template_name = "status_table.html"
    context_object_name = "statuses"
    extra_context = {
        "title": _("Statuses"),
        "button_text": _("Create status"),
    }


class StatusCreateView(UserLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    """
    The view shows create form for new status.
    Authorization required.
    """
    # CreateView attrs
    model = Status
    template_name = "form.html"
    form_class = StatusForm
    extra_context = {
        "title": _("Create status"),
        "button_text": _("Create"),
        "needs_messages": True,
    }
    success_url = reverse_lazy('list_status')
    # SuccessMessageMixin attrs
    success_message = _("Status successfully created")


class StatusUpdateView(UserLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    """
    Statuses update form.
    """
    # UpdateView attrs
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('list_status')
    extra_context = {
        "title": _("Change of status"),
        "button_text": _("Edit"),
        "needs_messages": True,
    }
    # SuccessMessageMixin attrs
    success_message = _("Status successfully changed")


class StatusDeleteView(UserLoginRequiredMixin,
                       TaskManagerFormMixin,
                       ProtectObjectDeletionMixin,
                       SuccessMessageMixin,
                       DeleteView):
    """
    Delete status.
    Authorization is required.
    Status may be deleted only if it isn't used.
    """
    # DeleteView attrs
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('list_status')
    extra_context = {
        "title": _("Status deletion"),
        "url_for_delete": "delete_status",
    }
    # SuccessMessageMixin attrs
    success_message = _("Status is successfully deleted")
