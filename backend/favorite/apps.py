"""Настройки приложения favorite."""
from django.apps import AppConfig


class FavoriteConfig(AppConfig):
    """Класс настроек приложения favorite."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favorite'
    verbose_name = 'Избранное'
