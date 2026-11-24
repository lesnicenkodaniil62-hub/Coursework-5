"""
Инициализация пакета config: подключаем Celery-приложение.
config package initialization: wire up the Celery app.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
