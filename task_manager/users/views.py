from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from task_manager.permission_mixins import UserLoginRequiredMixin
from task_manager.permission_mixins import UserPermissionTestMixin
from task_manager.users.forms import UserRegistrationForm
from task_manager.users.forms import UserUpdateForm
from task_manager.users.models import User


class UserIndexView(ListView):
    """List all User objects."""
    model = User
    template_name = "users_table.html"
    context_object_name = "users"
    # Optimize orm query and exclude admin
    queryset = User.objects.exclude(is_superuser=True).values(
        'id',
        'username',
        'date_joined',
        'first_name',
        'last_name'
    )


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
