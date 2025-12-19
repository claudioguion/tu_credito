from django.contrib import admin
from .models import Credit


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "credit_type",
        "status",
        "client",
        "bank",
        "minimum_payment",
        "maximum_payment",
        "term_months",
        "registered_date",
    ]

    list_filter = [
        "credit_type",
        "status",
        "bank",
    ]

    search_fields = [
        "description",
        "client__full_name",
        "client__document_id",
    ]

    ordering = [
        "-registered_date",
    ]

