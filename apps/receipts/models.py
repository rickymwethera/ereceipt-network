from django.conf import settings
from django.db import models


class Receipt(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        VALID = "valid", "Valid"
        INVALID = "invalid", "Invalid"
        MISSING_BUYER_PIN = "missing_buyer_pin", "Missing Buyer PIN"
        WRONG_BUYER_PIN = "wrong_buyer_pin", "Wrong Buyer PIN"
        UNREADABLE = "unreadable", "Unreadable"
        ERROR = "error", "Error"

    class Source(models.TextChoices):
        WEB = "web", "Web"
        WHATSAPP = "whatsapp", "WhatsApp"

    business = models.ForeignKey(
        "accounts.Business", on_delete=models.CASCADE, related_name="receipts"
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_receipts",
    )
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.WEB)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    invoice_number = models.CharField(max_length=50, blank=True, default="")
    supplier_pin = models.CharField(max_length=11, blank=True, default="")
    supplier_name = models.CharField(max_length=255, blank=True, default="")
    buyer_pin = models.CharField(max_length=11, blank=True, default="")
    invoice_date = models.DateField(null=True, blank=True)
    total_cents = models.PositiveBigIntegerField(null=True, blank=True)
    kra_checked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "invoice_number"],
                condition=~models.Q(invoice_number=""),
                name="unique_invoice_per_business",
            ),
        ]

    def __str__(self):
        return f"{self.invoice_number or 'No number'} - {self.get_status_display()}"
