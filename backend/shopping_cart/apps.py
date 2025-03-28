"""Настройки приложения shopping_cart."""
from django.apps import AppConfig


class ShoppingCartConfig(AppConfig):
    """Класс настроек приложения shopping_cart."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping_cart'
    verbose_name = 'Список покупок'
