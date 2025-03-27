"""Модели ingredients."""
import os

from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=int(os.getenv('INGREDIENT_NAME_MAX_LENGTH', '128')),
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=int(os.getenv('MEASUREMENT_UNIT_MAX_LENGTH', '64')),
        verbose_name='Единицы измерения'
    )

    class Meta:
        """Мета-информация Ingredient."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'measurement_unit')

    def __str__(self):
        """Строковое представление ингредиента."""
        return f'{self.name} ({self.measurement_unit})'
