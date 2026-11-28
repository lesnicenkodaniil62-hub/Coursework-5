"""
Сериализаторы приложения users.
Serializers of the users app.
"""

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Профиль пользователя: данные для уведомлений.
    User profile: notification delivery data.
    """

    class Meta:
        model = UserProfile
        fields = ("telegram_chat_id",)


class UserSerializer(serializers.ModelSerializer):
    """
    Данные текущего пользователя вместе с профилем.
    Поддерживает обновление telegram_chat_id через PATCH.
    Current user data together with the profile.
    Supports updating telegram_chat_id via PATCH.
    """

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "profile")
        read_only_fields = ("id", "username")

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        """
        Обновляет пользователя и вложенный профиль.
        Updates the user and the nested profile.
        """
        profile_data = validated_data.pop("profile", None)

        # Обновляем поля пользователя
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем профиль
        if profile_data is not None:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация нового пользователя.
    Registration of a new user.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2")
        read_only_fields = ("id",)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Проверяет совпадение паролей.
        Checks that both passwords match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Создаёт пользователя с хешированным паролем.
        Creates a user with a hashed password.
        """
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)
