"""Настройки приложения avatar_user."""
from django.apps import AppConfig


class AvatarUserConfig(AppConfig):
    """Класс настроек приложения avatar_user."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'avatar_user'
    verbose_name = 'Пользователи'
