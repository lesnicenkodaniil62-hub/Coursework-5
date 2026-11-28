"""
Представления приложения users.
Views of the users app.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import RegisterSerializer, UserSerializer


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
# Данные текущего пользователя: чтение и обновление
# ============================================
# Current user data: read and update
# ============================================
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        user: User = self.request.user  # type: ignore[assignment]
        return user
