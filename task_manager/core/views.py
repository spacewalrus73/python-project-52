from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView


class UserIndexView(TemplateView):
    """Shows home page."""
    template_name = "home.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    """Shows form and log in user."""
    # LoginView attrs
    template_name = "form.html"
    next_page = reverse_lazy("home")
    extra_context = {
        "title": _("Enter"),
        "button_text": _("Log in"),
    }
    # CustomSuccessMessageMixin attrs
    success_message = _("You're logged in")


class UserLogoutView(LogoutView):
    """Log out user."""
    next_page = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(
            request=request,
            level=messages.INFO,
            message=_("You're logged out"),
        )
        return HttpResponseRedirect(self.next_page)
