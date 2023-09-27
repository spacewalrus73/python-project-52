from .models import User
from django.db.models import CharField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):

    field_order = ['first_name', 'last_name', 'username', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):

        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')
