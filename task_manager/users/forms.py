from .models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("First name"))
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Last name")
    )

    field_order = ['first_name', 'last_name', 'username', 'password1', 'password2']
    help_texts = {
        'password1': _("Your password must contain at least 3 characters.")
    }

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')
