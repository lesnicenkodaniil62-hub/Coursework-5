"""
Сигналы приложения users.
Signals of the users app.
"""

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile


# ============================================
# Профиль создаётся автоматически при создании пользователя.
# Флаг raw=True означает загрузку фикстур — тогда профиль не создаём,
# чтобы не конфликтовать с данными из фикстуры.
# ============================================
# The profile is created automatically when a user is created.
# The raw=True flag means fixture loading — skip creation then
# to avoid conflicting with the fixture data.
# ============================================
@receiver(post_save, sender=User)
def create_user_profile(
    sender: type[User],
    instance: User,
    created: bool,
    raw: bool = False,
    **kwargs: Any,
) -> None:
    """
    Создаёт профиль для нового пользователя.
    Creates a profile for a newly created user.
    """
    if created and not raw:
        UserProfile.objects.get_or_create(user=instance)
