from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeletionMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UserLoginRequiredMixin(LoginRequiredMixin):
    """Verify that the current task_manager user is authenticated."""

    login_url = reverse_lazy("login")
    denied_message = _(
        "You are not authorised! Please log in."
    )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message=self.denied_message,
                extra_tags='danger'
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserPermissionTestMixin(UserPassesTestMixin):
    """
    Deny request if the user is trying to change staff,
    that do not belong to him.
    """

    redirect_url = reverse_lazy("list_user")
    permission_denied_message = _(
        "You don't have the rights to modify another user."
    )

    def test_func(self):
        """Testing that the current user is the owner."""
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message=self.permission_denied_message,
                extra_tags='danger'
                )
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class ProtectObjectDeletionMixin(DeletionMixin):
    """Deny deletion if object is used by other object."""

    denied_url = None
    protect_message = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message=self.protect_message,
            )
            return redirect(self.denied_url)


class TaskManagerFormMixin(FormMixin):

    def get_context_data(self, **kwargs):
        """Displays object's name to be deleted."""
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context["obj_name"] = obj.name
        return context
