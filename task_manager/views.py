from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin


class Index(TemplateView):

    template_name = 'home.html'


class UserLogin(SuccessMessageMixin, LoginView):

    template_name = 'login.html'
    success_message = _("You're logged in")

    def get_success_url(self):
        return reverse_lazy('index')


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, _("You're unlogged"))
    return redirect('login')
