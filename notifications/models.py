"""
Модели приложения notifications: журнал отправленных напоминаний.
Models of the notifications app: the log of sent reminders.
"""

from django.db import models

from habits.models import Habit


class ReminderLog(models.Model):
    """
    Запись об отправленном напоминании. Нужна для соблюдения периодичности.
    A record of a sent reminder. Used to respect the habit periodicity.
    """

    # ============================================
    # Привычка, о которой напомнили
    # ============================================
    # The habit that was reminded about
    # ============================================
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="reminder_logs",
        verbose_name="Привычка",
    )

    # ============================================
    # Дата отправки напоминания
    # ============================================
    # Date when the reminder was sent
    # ============================================
    sent_date = models.DateField(verbose_name="Дата напоминания")

    # ============================================
    # Точное время создания записи
    # ============================================
    # Exact time when the record was created
    # ============================================
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Журнал напоминаний"
        verbose_name_plural = "Журнал напоминаний"
        ordering = ["-sent_date"]
        # ============================================
        # Одна запись на привычку в день: защита от повторной отправки
        # ============================================
        # One record per habit per day: protection against duplicate sending
        # ============================================
        constraints = [
            models.UniqueConstraint(fields=["habit", "sent_date"], name="unique_reminder_per_day"),
        ]

    def __str__(self) -> str:
        """
        Строковое представление записи журнала.
        String representation of the log record.
        """
        return f"{self.habit.action} — {self.sent_date}"
