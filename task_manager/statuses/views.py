from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm, StatusUpdateForm
from task_manager.permission_mixins import (
    UserLoginRequiredMixin,
    TaskManagerFormMixin,
    ProtectObjectDeletionMixin
)


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
    form_class = StatusCreationForm
    extra_context = {
        "title": _("Create status"),
        "button_text": _("Create"),
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
    form_class = StatusUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('list_status')
    extra_context = {
        "title": _("Change of status"),
        "button_text": _("Edit"),
    }
    #SuccessMessageMixin attrs
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
