"""
Celery-задачи приложения notifications.
Celery tasks of the notifications app.
"""

import logging

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from notifications.services import build_reminder_text, send_telegram_message

logger = logging.getLogger(__name__)


# ============================================
# Задача запускается каждую минуту Celery Beat.
# Напоминание отправляется по каждой привычке, у которой
# наступило время выполнения и соблюдена периодичность.
# ============================================
# The task is triggered every minute by Celery Beat.
# A reminder is sent for every habit whose time has come
# and whose periodicity is respected.
# ============================================
@shared_task
def send_habit_reminders() -> int:
    """
    Рассылает напоминания и возвращает число отправленных сообщений.
    Sends reminders and returns the number of delivered messages.
    """
    now = timezone.localtime()
    today = now.date()

    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
    ).select_related("owner", "owner__profile", "related_habit")

    sent = 0
    for habit in habits:
        # ============================================
        # Соблюдаем периодичность: не чаще, чем раз в N дней
        # ============================================
        # Respect the periodicity: no more often than once every N days
        # ============================================
        if habit.last_reminded_at is not None and (today - habit.last_reminded_at).days < habit.periodicity:
            continue

        # ============================================
        # Профиль может отсутствовать или быть без chat_id
        # ============================================
        # The profile may be missing or have no chat_id
        # ============================================
        profile = getattr(habit.owner, "profile", None)
        chat_id = getattr(profile, "telegram_chat_id", None)
        if not chat_id:
            continue

        if send_telegram_message(chat_id, build_reminder_text(habit)):
            habit.last_reminded_at = today
            habit.save(update_fields=["last_reminded_at"])
            sent += 1

    logger.info("Отправлено напоминаний: %s", sent)
    return sent
