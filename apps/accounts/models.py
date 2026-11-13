from django.conf import settings
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


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        STAFF = "staff", "Staff"
        ACCOUNTANT = "accountant", "Accountant"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "business"], name="unique_membership"),
        ]

    def __str__(self):
        return f"{self.user} - {self.business} ({self.get_role_display()})"
