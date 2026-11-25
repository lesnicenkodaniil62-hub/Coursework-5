"""
Админка приложения habits.
Admin configuration of the habits app.
"""

from django.contrib import admin

from .models import Habit


# ============================================
# Отображение привычек в админке
# ============================================
# Habit representation in the admin site
# ============================================
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "owner", "time", "is_pleasant", "is_public", "periodicity")
    list_filter = ("is_pleasant", "is_public", "periodicity")
    search_fields = ("action", "place", "owner__username")
