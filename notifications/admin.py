"""
Админка приложения notifications.
Admin configuration of the notifications app.
"""

from django.contrib import admin

from notifications.models import ReminderLog


# ============================================
# Журнал напоминаний доступен только для просмотра
# ============================================
# The reminder log is read-only in the admin site
# ============================================
@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ("id", "habit", "sent_date", "created_at")
    list_filter = ("sent_date",)
    search_fields = ("habit__action",)
