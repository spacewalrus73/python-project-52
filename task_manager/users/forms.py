from .models import User
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm


class UserRegistrationForm(UserCreationForm):

    field_order = [
        'first_name',
        'last_name',
        'username',
        'password1',
        'password2',
    ]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class UserUpdateForm(BaseUserCreationForm):

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
