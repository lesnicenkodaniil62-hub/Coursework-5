"""
Права доступа приложения habits.
Access permissions of the habits app.
"""

from typing import Any

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from habits.models import Habit
from users.models import User


# ============================================
# Полный доступ только владельцу привычки
# ============================================
# Full access is granted to the habit owner only
# ============================================
class IsOwner(BasePermission):
    message = "У вас нет прав на изменение этой привычки."

    def has_object_permission(self, request: Request, view: APIView, obj: Habit) -> bool:
        user: User | AnonymousUser = request.user
        return bool(user.is_authenticated and obj.owner_id == user.pk)


# ============================================
# Аутентифицированный пользователь читает публичные привычки,
# но редактировать и удалять может только свои
# ============================================
# An authenticated user reads public habits,
# but may edit and delete only their own ones
# ============================================
class IsOwnerOrPublicReadOnly(BasePermission):
    message = "Публичные привычки доступны только для чтения."

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user: User | AnonymousUser = request.user
        if not user.is_authenticated:
            return False
        if obj.owner_id == user.pk:
            return True
        return bool(request.method in SAFE_METHODS and getattr(obj, "is_public", False))
