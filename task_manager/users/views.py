from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from task_manager.settings import ADMIN_ID
from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm, UserUpdateForm
from task_manager.permission_mixins import (
    UserLoginRequiredMixin,
    UserPermissionTestMixin
)


class UserIndexView(ListView):
    """List all User objects."""
    model = User
    template_name = "users_table.html"
    context_object_name = "users"

    def get_queryset(self):
        """Excludes admin from users list."""
        return super().get_queryset().exclude(id=ADMIN_ID)


class UserCreateView(SuccessMessageMixin, CreateView):
    """Users create form."""
    # CreateView attrs
    model = User
    template_name = "form.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    extra_context = {
        "title": _("Registration"),
        "button_text": _("Register"),
    }
    # SuccessMessageMixin attrs
    success_message = _("User is successfully registered")


class UserUpdateView(UserLoginRequiredMixin,
                     UserPermissionTestMixin,
                     SuccessMessageMixin,
                     UpdateView):
    """
    Users update form.
    Authentication required. Only user can edit himself.
    """
    # UpdateView attrs
    model = User
    form_class = UserUpdateForm
    template_name = "form.html"
    success_url = reverse_lazy("list_user")
    extra_context = {
        "title": _("Update user"),
        "button_text": _("Update"),
    }
    # SuccessMessageMixin attrs
    success_message = _("User successfully changed")


class UserDeleteView(UserLoginRequiredMixin,
                     UserPermissionTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    """
    User's deletion view. Authentication required.
    Only user can delete himself.
    """
    # DeleteView attrs
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('list_user')
    extra_context = {
        "title": _('User deletion'),
        "url_for_delete": "delete_user",
    }
    # SuccessMessageMixin attrs
    success_message = _("User successfully deleted")
