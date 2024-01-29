from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default task manager's user"""

    def get_name(self) -> str:
        return self.get_full_name()
