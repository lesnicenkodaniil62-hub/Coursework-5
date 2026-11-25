"""
Конфигурация приложения users.
Configuration of the users app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения пользователей.
    Configuration of the users application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"

    def ready(self) -> None:
        """
        Подключает обработчики сигналов при старте приложения.
        Registers signal handlers on application startup.
        """
        from . import signals  # noqa: F401
