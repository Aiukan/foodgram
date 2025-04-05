"""Модели tags."""
from django.db import models

from foodgram_backend.constants import (TAGS_NAME_MAX_LENGTH,
                                        TAGS_SLUG_MAX_LENGTH)


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=TAGS_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=TAGS_SLUG_MAX_LENGTH,
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
        return f'Тег {self.name}'
