from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "seller",
        "gemstone_type",
        "price",
        "quantity",
        "status",
        "is_ai_verified",
        "created_at",
    )

    list_filter = (
        "gemstone_type",
        "condition",
        "status",
        "is_ai_verified",
        "created_at",
    )

    search_fields = (
        "title",
        "seller__username",
        "seller__email",
        "origin",
        "color",
    )

    readonly_fields = (
        "seller",
        "ai_prediction",
        "ai_confidence",
        "is_ai_verified",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Seller Information", {
            "fields": ("seller",)
        }),

        ("Gemstone Details", {
            "fields": (
                "title",
                "gemstone_type",
                "description",
                "price",
                "weight",
                "color",
                "origin",
                "shape",
                "dimensions",
                "treatment",
                "certification",
                "quantity",
                "condition",
                "status",
            )
        }),

        ("AI Verification", {
            "fields": (
                "ai_prediction",
                "ai_confidence",
                "is_ai_verified",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),

    )

    inlines = [ListingImageInline]


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "listing",
        "uploaded_at",
    )

    search_fields = (
        "listing__title",
    )