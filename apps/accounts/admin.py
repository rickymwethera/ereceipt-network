from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Business, Membership, User

admin.site.register(User, UserAdmin)


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["name", "kra_pin", "created_at"]
    search_fields = ["name", "kra_pin"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "business", "role", "created_at"]
    list_filter = ["role"]
