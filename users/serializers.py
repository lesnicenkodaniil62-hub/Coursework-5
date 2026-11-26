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
    Current user data together with the profile.
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "profile")
        read_only_fields = ("id", "username")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация нового пользователя.
    Registration of a new user.
    """

    # ============================================
    # Пароль только для записи, проверяется валидаторами Django
    # ============================================
    # The password is write-only and checked by Django validators
    # ============================================
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
