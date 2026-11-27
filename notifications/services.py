"""
Сервис отправки сообщений в Telegram.
Service for sending messages to Telegram.
"""

import logging

import requests
from django.conf import settings

from habits.models import Habit

logger = logging.getLogger(__name__)

# ============================================
# Таймаут запроса к Telegram API в секундах
# ============================================
# Timeout for a Telegram API request in seconds
# ============================================
REQUEST_TIMEOUT = 10


def send_telegram_message(chat_id: str, text: str) -> bool:
    """
    Отправляет сообщение в указанный чат. Возвращает признак успеха.
    Sends a message to the given chat. Returns a success flag.
    """
    token: str = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN не задан, отправка пропущена.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # ============================================
    # Сетевые ошибки не должны ронять задачу рассылки
    # ============================================
    # Network errors must not break the reminder task
    # ============================================
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Не удалось отправить сообщение в чат %s.", chat_id)
        return False

    return True


def build_reminder_text(habit: Habit) -> str:
    """
    Формирует текст напоминания по формуле книги.
    Builds the reminder text following the book formula.
    """
    lines = [f"Напоминание: я буду {habit.action} в {habit.time:%H:%M} в {habit.place}"]

    # ============================================
    # Вознаграждение: либо приятная привычка, либо произвольное
    # ============================================
    # Reward: either a pleasant habit or a custom one
    # ============================================
    if habit.related_habit is not None:
        lines.append(f"Приятное после выполнения: {habit.related_habit.action}")
    elif habit.reward:
        lines.append(f"Вознаграждение: {habit.reward}")

    lines.append(f"Время на выполнение: {habit.execution_time} сек.")
    return "\n".join(lines)
