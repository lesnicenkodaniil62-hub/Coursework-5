"""
Сериализаторы приложения habits.
Serializers of the habits app.
"""

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.request import Request

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор привычки с подключением модельной валидации.
    Habit serializer wired to the model-level validation.
    """

    # ============================================
    # Владелец проставляется автоматически и недоступен для записи
    # ============================================
    # The owner is assigned automatically and is read-only
    # ============================================
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Habit
        fields = (
            "id",
            "owner",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
        )
        read_only_fields = ("id", "owner")

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Прогоняет кросс-полевые проверки модели через clean().
        Runs the model cross-field checks via clean().
        """
        validated: dict[str, Any] = super().validate(attrs)

        # ============================================
        # Собираем экземпляр: для обновления берём существующий объект
        # и переносим на него новые значения, для создания — новый.
        # Сохранение не выполняем, нужна только валидация.
        # ============================================
        # Build an instance: on update reuse the existing object
        # and apply the incoming values, on create build a new one.
        # Nothing is saved, validation only.
        # ============================================
        data: dict[str, Any] = {}
        if self.instance is not None:
            for field in self.Meta.fields:
                if field not in ("id", "owner", "related_habit"):
                    data[field] = getattr(self.instance, field)
            data["related_habit"] = self.instance.related_habit
        data.update(validated)

        habit = Habit(**data)

        request: Request | None = self.context.get("request")
        if request is not None and request.user.is_authenticated:
            habit.owner_id = request.user.pk

        # ============================================
        # clean_fields проверяет поля, clean — кросс-полевые правила.
        # Ошибки Django превращаем в ошибки DRF.
        # ============================================
        # clean_fields validates fields, clean validates cross-field rules.
        # Django errors are converted into DRF errors.
        # ============================================
        try:
            habit.clean_fields(exclude=["owner"])
            habit.clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

        return validated
