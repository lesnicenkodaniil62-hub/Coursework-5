"""
Модели приложения users.
Models of the users app.
"""

from django.contrib.auth.models import AbstractUser


# ============================================
# Кастомная модель пользователя. Пока наследует AbstractUser,
# расширения (профиль, telegram_chat_id) добавим в Фиче 2.
# ============================================
# Custom user model. Inherits AbstractUser for now;
# extensions (profile, telegram_chat_id) come in Feature 2.
# ============================================
class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
