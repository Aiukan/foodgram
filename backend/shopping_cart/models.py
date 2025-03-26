from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class ShoppingCart(models.Model):
    """Модель записи списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        """Мета-информация ShoppingCart."""

        verbose_name = 'Запись списка покупок'
        verbose_name_plural = 'Записи списка покупок'
        unique_together = ('recipe', 'user')

    def __str__(self):
        """Строковое представление записи списка покупок."""
        return f'Запись: {self.user} - {self.recipe}.'
