"""Настройки приложения api."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Класс настроек api."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
