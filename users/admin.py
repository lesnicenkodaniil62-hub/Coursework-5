"""
Админка приложения users.
Admin configuration of the users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


# ============================================
# Пользователи в админке
# ============================================
# Users in the admin site
# ============================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")


# ============================================
# Профили пользователей в админке
# ============================================
# User profiles in the admin site
# ============================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "telegram_chat_id")
    search_fields = ("user__username", "telegram_chat_id")
