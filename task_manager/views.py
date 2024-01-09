from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin


class Index(TemplateView):

    template_name = 'home.html'


class UserLogin(SuccessMessageMixin, LoginView):

    template_name = 'registration/login.html'
    success_message = _("You're logged in")

    def get_success_url(self):
        return reverse('index')


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, _("You're logged out"))
    return redirect('login')
