"""
Представления приложения habits.
Views of the habits app.
"""

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner, IsOwnerOrPublicReadOnly
from habits.serializers import HabitSerializer
from users.models import User


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD привычек текущего пользователя.
    CRUD for the habits of the current user.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = HabitPagination

    def get_queryset(self) -> QuerySet[Habit]:
        """
        Пользователь видит и изменяет только свои привычки.
        The user sees and modifies only their own habits.
        """
        user: User = self.request.user  # type: ignore[assignment]
        return Habit.objects.filter(owner=user).select_related("owner", "related_habit")

    def perform_create(self, serializer: BaseSerializer[Habit]) -> None:
        """
        Владелец проставляется из текущего пользователя.
        The owner is taken from the current user.
        """
        serializer.save(owner=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Список публичных привычек — только чтение.
    List of public habits — read only.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrPublicReadOnly)
    pagination_class = HabitPagination
    queryset = Habit.objects.filter(is_public=True).select_related("owner", "related_habit")
