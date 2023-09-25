from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from task_manager.users.models import User
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin


class UserIndex(ListView):

    model = User
    paginate_by = 60
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreate(CreateView, SuccessMessageMixin):

    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('create_user')
    success_message = _("User is successfully registered")
