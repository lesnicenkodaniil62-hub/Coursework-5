"""
Точка входа Celery для проекта.
Celery entry point for the project.
"""

import os

from celery import Celery
from celery.schedules import crontab

# ============================================
# Модуль настроек Django по умолчанию
# ============================================
# Default Django settings module
# ============================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# ============================================
# Конфигурация из настроек Django с префиксом CELERY
# ============================================
# Configuration from Django settings with the CELERY prefix
# ============================================
app.config_from_object("django.conf:settings", namespace="CELERY")

# ============================================
# Автообнаружение задач в приложениях
# ============================================
# Autodiscover tasks in installed apps
# ============================================
app.autodiscover_tasks()

# ============================================
# Расписание: проверка привычек каждую минуту
# ============================================
# Schedule: check habits every minute
# ============================================
app.conf.beat_schedule = {
    "send-habit-reminders-every-minute": {
        "task": "notifications.tasks.send_habit_reminders",
        "schedule": crontab(minute="*"),
    },
}
