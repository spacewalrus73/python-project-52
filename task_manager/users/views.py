from django.urls import reverse_lazy
from task_manager.users.models import User
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .permissions_mixins import (
    UserLoginRequiredMixin,
    UserRightsPassesTestMixin
)

class UserIndex(ListView):
    """
    List all User objects
    """
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreate(SuccessMessageMixin, CreateView):
    """
    The view shows create form for new users - UserRegistrationForm
    """
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    success_message = _("User is successfully registered")


class UserUpdate(UserLoginRequiredMixin,
                 UserRightsPassesTestMixin,
                 SuccessMessageMixin,
                 UpdateView):
    """
    User's updates form
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/updating.html'
    context_object_name = 'user'
    success_url = reverse_lazy('list_user')
    success_message = _("User successfully changed")


class UserDelete(UserLoginRequiredMixin,
                 UserRightsPassesTestMixin,
                 SuccessMessageMixin,
                 DeleteView):
    """
    User's deletion view
    """
    model = User
    template_name = 'users/deletion.html'
    context_object_name = 'user'
    success_url = reverse_lazy('list_user')
    success_message = _("User successfully deleted")
