"""
Сервис отправки сообщений в Telegram.
Service for sending messages to Telegram.
"""

import logging
from typing import Any

import requests
from django.conf import settings

from habits.models import Habit

logger = logging.getLogger(__name__)

# ============================================
# Таймаут запроса к Telegram API в секундах
# ============================================
# Timeout for a Telegram API request in seconds
# ============================================
REQUEST_TIMEOUT = 30


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
    # Необязательный прокси: нужен, если API недоступен напрямую
    # ============================================
    # Optional proxy: used when the API is not reachable directly
    # ============================================
    proxy: str = settings.TELEGRAM_PROXY
    proxies = {"http": proxy, "https": proxy} if proxy else None

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
            proxies=proxies,
        )
    except requests.RequestException:
        logger.exception("Сетевая ошибка при отправке в чат %s.", chat_id)
        return False

    # ============================================
    # Разбираем ответ Telegram: он может отклонить сообщение
    # ============================================
    # Parse the Telegram reply: it may reject the message
    # ============================================
    try:
        data: dict[str, Any] = response.json()
    except ValueError:
        logger.error("Некорректный ответ Telegram: %s", response.text[:200])
        return False

    if not data.get("ok"):
        logger.error(
            "Telegram отклонил сообщение в чат %s: %s",
            chat_id,
            data.get("description"),
        )
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
