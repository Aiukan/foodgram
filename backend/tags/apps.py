"""Настройки приложения tags."""
from django.apps import AppConfig


class TagsConfig(AppConfig):
    """Класс настроек приложения tags."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'
    verbose_name = 'Теги'
