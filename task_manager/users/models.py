from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default task manager's user"""

    def __str__(self):
        return self.get_full_name()
