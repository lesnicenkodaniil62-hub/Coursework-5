"""
Представления приложения users.
Views of the users app.
"""

from typing import Any

from django.db.models import QuerySet
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, UserProfile
from users.serializers import RegisterSerializer, UserProfileSerializer, UserSerializer


# ============================================
# Регистрация доступна без авторизации
# ============================================
# Registration is available without authentication
# ============================================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


# ============================================
# Данные текущего пользователя
# ============================================
# Current user data
# ============================================
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        user: User = self.request.user  # type: ignore[assignment]
        return user


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Профили пользователей: каждый работает только со своим.
    User profiles: everyone works with their own profile only.
    """

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[UserProfile]:
        user: User = self.request.user  # type: ignore[assignment]
        return UserProfile.objects.filter(user=user).select_related("user")

    def perform_create(self, serializer: Any) -> None:
        serializer.save(user=self.request.user)
