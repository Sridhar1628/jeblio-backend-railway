from django.contrib import admin
from .models import TermsAndConditions, WebinarRegistration


@admin.register(TermsAndConditions)
class TermsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    search_fields = ("title",)


@admin.register(WebinarRegistration)
class WebinarRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "payment_id",
        "order_id",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "payment_id",
        "order_id",
    )

    list_filter = (
        "payment_status",
        "created_at",
    )

    readonly_fields = (
        "payment_id",
        "order_id",
        "created_at",
    )

from django.contrib import admin
from .models import WebinarLead


@admin.register(WebinarLead)
class WebinarLeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "order_id",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "order_id",
    )

    list_filter = (
        "payment_status",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Lead Information", {
            "fields": (
                "name",
                "email",
                "phone",
            )
        }),
        ("Payment Details", {
            "fields": (
                "order_id",
                "payment_status",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
            )
        }),
    )