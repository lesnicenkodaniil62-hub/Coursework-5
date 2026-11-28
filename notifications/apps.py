"""
Конфигурация приложения notifications.
Configuration of the notifications app.
"""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    Конфигурация приложения рассылки напоминаний.
    Configuration of the reminder delivery application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
    verbose_name = "Напоминания"
