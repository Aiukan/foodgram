"""Настройки приложения ingredients."""
from django.apps import AppConfig


class IngredientsConfig(AppConfig):
    """Класс настроек приложения ingredients."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingredients'
    verbose_name = 'Ингредиенты'
