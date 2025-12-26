from django.contrib import admin
from .models import Payment, Review


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "client",
        "freelancer",
        "total_amount",
        "admin_amount",
        "freelancer_amount",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "created_at",
    )

    search_fields = (
        "client__username",
        "freelancer__username",
        "project__title",
    )

    readonly_fields = (
        "admin_amount",
        "freelancer_amount",
        "created_at",
    )

    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "freelancer",
        "client",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "freelancer__username",
        "client__username",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)
