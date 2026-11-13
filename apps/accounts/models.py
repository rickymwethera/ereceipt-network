from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model.

    Set up before the first migration so you can add fields later
    (phone number, role, etc.) without a painful migration. Add fields here.
    """


class Business(models.Model):
    name = models.CharField(max_length=200)
    kra_pin = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
