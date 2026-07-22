from django.contrib import admin

# Register your models here.

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "buyer",
        "seller",
        "listing",
        "updated_at",
    )

    search_fields = (
        "buyer__username",
        "seller__username",
        "listing__title",
    )

    list_filter = (
        "updated_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "conversation",
        "sender",
        "is_read",
        "created_at",
    )

    search_fields = (
        "sender__username",
        "message",
    )

    list_filter = (
        "is_read",
        "created_at",
    )