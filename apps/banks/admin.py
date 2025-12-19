from django.contrib import admin
from .models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "code",
        "address",
        "contact_email",
        "created_at",
    ]

    list_filter = [
        "type",
    ]

    search_fields = [
        "name",
        "code",
        "direction",
        "contact_email",
    ]
