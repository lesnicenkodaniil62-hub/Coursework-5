"""
Модели приложения habits: привычка и её валидация.
Models of the habits app: the habit and its validation.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# ============================================
# Максимальное время выполнения привычки в секундах (по книге — 2 минуты)
# ============================================
# Maximum habit execution time in seconds (per the book — 2 minutes)
# ============================================
MAX_EXECUTION_TIME = 120

# ============================================
# Максимальная периодичность: не реже одного раза в 7 дней
# ============================================
# Maximum periodicity: at least once every 7 days
# ============================================
MAX_PERIODICITY = 7


class Habit(models.Model):
    """
    Привычка по формуле: я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО].
    A habit following the formula: I will [ACTION] at [TIME] in [PLACE].
    """

    # ============================================
    # Пользователь — создатель привычки
    # ============================================
    # User — the owner who created the habit
    # ============================================
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )

    # ============================================
    # Место выполнения привычки
    # ============================================
    # Place where the habit is performed
    # ============================================
    place = models.CharField(max_length=255, verbose_name="Место")

    # ============================================
    # Время, когда необходимо выполнять привычку
    # ============================================
    # Time when the habit must be performed
    # ============================================
    time = models.TimeField(verbose_name="Время")

    # ============================================
    # Действие, которое представляет собой привычка
    # ============================================
    # The action that constitutes the habit
    # ============================================
    action = models.CharField(max_length=255, verbose_name="Действие")

    # ============================================
    # Признак приятной привычки: приятная служит вознаграждением
    # ============================================
    # Pleasant habit flag: a pleasant habit acts as a reward
    # ============================================
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")

    # ============================================
    # Связанная привычка: только приятная, указывается для полезных привычек
    # ============================================
    # Related habit: must be pleasant, used for useful habits
    # ============================================
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="used_as_reward_in",
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )

    # ============================================
    # Периодичность выполнения в днях, по умолчанию ежедневная
    # ============================================
    # Execution periodicity in days, daily by default
    # ============================================
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(MAX_PERIODICITY)],
        verbose_name="Периодичность (в днях)",
        help_text="От 1 до 7 дней: нельзя выполнять привычку реже одного раза в неделю.",
    )

    # ============================================
    # Вознаграждение за выполнение полезной привычки
    # ============================================
    # Reward for performing a useful habit
    # ============================================
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")

    # ============================================
    # Время на выполнение в секундах, не более 120
    # ============================================
    # Execution time in seconds, no more than 120
    # ============================================
    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(MAX_EXECUTION_TIME)],
        verbose_name="Время на выполнение (в секундах)",
        help_text="Не более 120 секунд.",
    )

    # ============================================
    # Признак публичности: привычку видят другие пользователи
    # ============================================
    # Public flag: the habit is visible to other users
    # ============================================
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    # ============================================
    # Дата последнего отправленного напоминания.
    # Служебное поле: не редактируется вручную и не отдаётся в API.
    # ============================================
    # Date of the last sent reminder.
    # Internal field: not editable manually and not exposed via the API.
    # ============================================
    last_reminded_at = models.DateField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="Дата последнего напоминания",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id"]

    def __str__(self) -> str:
        """
        Строковое представление по формуле книги.
        String representation following the book formula.
        """
        return f"{self.action} в {self.time} в {self.place}"

    def clean(self) -> None:
        """
        Кросс-полевая валидация привычки.
        Cross-field validation of the habit.
        """
        super().clean()

        errors: dict[str, str] = {}
        has_related = self.related_habit_id is not None

        if self.is_pleasant:
            # ============================================
            # У приятной привычки не может быть вознаграждения
            # ============================================
            # A pleasant habit cannot have a reward
            # ============================================
            if self.reward:
                errors["reward"] = "У приятной привычки не может быть вознаграждения."

            # ============================================
            # У приятной привычки не может быть связанной привычки
            # ============================================
            # A pleasant habit cannot have a related habit
            # ============================================
            if has_related:
                errors["related_habit"] = "У приятной привычки не может быть связанной привычки."
        else:
            # ============================================
            # Нельзя одновременно указать вознаграждение и связанную привычку
            # ============================================
            # A reward and a related habit cannot be set at the same time
            # ============================================
            if self.reward and has_related:
                errors["related_habit"] = "Нельзя одновременно выбрать связанную привычку и указать вознаграждение."

            # ============================================
            # В связанные привычки попадают только приятные привычки
            # ============================================
            # Only pleasant habits may be used as a related habit
            # ============================================
            if has_related and self.related_habit is not None and not self.related_habit.is_pleasant:
                errors["related_habit"] = "В связанные привычки могут попадать только приятные привычки."

        if errors:
            raise ValidationError(errors)
