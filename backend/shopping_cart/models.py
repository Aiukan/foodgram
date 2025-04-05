"""Модели shopping_cart."""
from django.contrib.auth import get_user_model
from django.db import models

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

        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_shoppingcart'
            ),
        )

    def __str__(self):
        """Строковое представление записи списка покупок."""
        return f'{self.recipe} в списке покупок у {self.user}.'
