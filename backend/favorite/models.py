"""Модели favorite."""
from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    """Модель добавления в избранное."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='farovite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='farovite_users'
    )

    class Meta:
        """Мета-информация Favorite."""

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('recipe', 'user')

    def __str__(self):
        """Строковое представление избранного."""
        return f'{self.recipe} в избранном у {self.user}.'
