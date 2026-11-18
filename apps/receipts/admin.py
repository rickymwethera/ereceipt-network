from django.contrib import admin

from .models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "business", "status", "total_cents", "created_at"]
    list_filter = ["status", "source", "business"]
    search_fields = ["invoice_number", "supplier_name", "supplier_pin"]
