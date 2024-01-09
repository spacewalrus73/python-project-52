from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UserLoginRequiredMixin(LoginRequiredMixin):
    """Verify that the current task_manager_user is authenticated"""

    login_url = reverse_lazy('login')
    denied_message = _("You are not authorised! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                self.denied_message,
                extra_tags='danger'
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AppPassesTestMixin(UserPassesTestMixin):
    """
    Deny request if the user is trying to change staff,
    that don't belong to him.
    """

    denied_url = reverse_lazy('list_user')
    denied_message = _("You don't have the rights to modify another user.")

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(
                request,
                messages.ERROR,
                self.denied_message,
                extra_tags='danger'
                )
            return redirect(self.denied_url)
        return super().dispatch(request, *args, **kwargs)


class UserRightsPassesTestMixin(AppPassesTestMixin):
    """Only the user has access to modify and delete staff about themselves"""
    def test_func(self):
        return self.get_object() == self.request.user
