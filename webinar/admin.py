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