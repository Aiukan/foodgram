"""Модели ingredients."""
from django.db import models

from foodgram_backend.constants import (INGREDIENT_NAME_MAX_LENGTH,
                                        MEASUREMENT_UNIT_MAX_LENGTH)


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единицы измерения'
    )

    class Meta:
        """Мета-информация Ingredient."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'measurement_unit')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        """Строковое представление ингредиента."""
        return f'Ингредиент {self.name} ({self.measurement_unit})'
