from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model.

    Set up before the first migration so you can add fields later
    (phone number, role, etc.) without a painful migration. Add fields here.
    """
