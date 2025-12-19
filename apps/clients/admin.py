from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "person_type",
        "document_id",
        "email",
        "bank",
        "created_at",
    ]

    list_filter = [
        "person_type",
        "bank",
    ]

    search_fields = [
        "full_name",
        "document_id",
        "email"
    ]
