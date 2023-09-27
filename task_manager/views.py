from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy


class Index(TemplateView):

    template_name = 'home.html'


class UserLogin(LoginView):

    template_name = 'login.html'
    next_page = reverse_lazy('index')
