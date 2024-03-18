from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.permission_mixins import ProtectObjectDeletionMixin
from task_manager.permission_mixins import UserLoginRequiredMixin


class LabelIndexView(UserLoginRequiredMixin, ListView):
    """List all Label objects. Authentication required."""
    model = Label
    template_name = "list_objects.html"
    extra_context = {
        "title": _("Labels"),
        "button_text": _("Create label"),
        "button_class": "btn-success",
        "captions": [
            "Name", "Creation date",
        ],
        "url_to_create": reverse_lazy("create_label"),
        "url_to_update": "update_label",
        "url_to_delete": "delete_label",
    }


class LabelCreateView(UserLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    """Create view of label object."""
    model = Label
    form_class = LabelForm
    template_name = "form.html"

    extra_context = {
        "title": _("Create label"),
        "button_text": _("Create"),
        "needs_messages": True,
    }
    success_url = reverse_lazy("list_label")
    # SuccessMessageMixin
    success_message = _("Label successfully created")


class LabelUpdateView(UserLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    """Update label object."""
    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy('list_label')
    extra_context = {
        "title": _("Change of label"),
        "button_text": _("Edit"),
        "needs_messages": True,
    }
    # SuccessMessageMixin attrs
    success_message = _("Label successfully changed")


class LabelDeleteView(UserLoginRequiredMixin,
                      ProtectObjectDeletionMixin,
                      SuccessMessageMixin,
                      DeleteView):
    """Deletion view of label object."""
    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy('list_label')
    extra_context = {
        "title": _("Label deletion"),
        "url_for_delete": "delete_label",
    }
    # ProtectedObjectDeletionMixin
    denied_url = reverse_lazy("list_label")
    protect_message = _("Can't delete a label because it's related with task")
    # SuccessMessageMixin
    success_message = _("Label is successfully deleted")
