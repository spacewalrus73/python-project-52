from django.db.models import DateTimeField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default task manager's user"""
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.get_full_name()
