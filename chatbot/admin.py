from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ("message", "response", "created_at")
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "ip_address", "created_at")
    search_fields = ("ip_address",)
    list_filter = ("created_at",)
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "short_message", "short_response", "created_at")
    search_fields = ("message", "response")
    list_filter = ("created_at",)

    def short_message(self, obj):
        return obj.message[:50]

    def short_response(self, obj):
        return obj.response[:50]