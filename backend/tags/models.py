"""Модели tags."""
import os

from django.db import models


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=int(os.getenv('TAGS_NAME_MAX_LENGTH', '64')),
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=int(os.getenv('TAGS_SLUG_MAX_LENGTH', '64')),
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        """Мета-информация Tag."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        """Строковое представление тега."""
        return f'{self.name}'
