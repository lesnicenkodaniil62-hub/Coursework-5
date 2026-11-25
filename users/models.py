"""
Модели приложения users: пользователь и его профиль.
Models of the users app: the user and their profile.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# ============================================
# Кастомная модель пользователя
# ============================================
# Custom user model
# ============================================
class User(AbstractUser):
    """
    Пользователь сервиса. Наследует стандартные поля Django.
    Service user. Inherits the standard Django fields.
    """

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserProfile(models.Model):
    """
    Профиль пользователя с данными для уведомлений.
    User profile holding data for notifications.
    """

    # ============================================
    # Связь с пользователем один к одному
    # ============================================
    # One-to-one link to the user
    # ============================================
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    # ============================================
    # Идентификатор чата Telegram для рассылки напоминаний
    # ============================================
    # Telegram chat identifier used for reminder delivery
    # ============================================
    telegram_chat_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Telegram chat ID",
        help_text="Заполняется для получения напоминаний в Telegram.",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self) -> str:
        """
        Строковое представление профиля.
        String representation of the profile.
        """
        return f"Профиль {self.user.username}"
