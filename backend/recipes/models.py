"""Модели recipws."""
import os

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class RecipeIngredient(models.Model):
    """Связь ингредиента и рецепта."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    amount = models.IntegerField(
        validators=(validators.MinValueValidator(1),),
        verbose_name='Количество'
    )

    class Meta:
        """Мета-информация RecipeIngredient."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ('recipe', 'ingredient')
        ordering = ('pk',)

    def __str__(self):
        """Строковое представление RecipeIngredient."""
        return f'{self.recipe} - {self.ingredient} ({self.amount})'


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        max_length=int(os.getenv('RECIPE_NAME_MAX_LENGTH', '256')),
        unique=True,
        verbose_name='Название'
    )
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        validators=(validators.MinValueValidator(1),),
        verbose_name='Время приготовления'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор'
    )

    class Meta:
        """Мета-информация Recipe."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date_created', 'name',)

    def __str__(self):
        """Строковое представление рецепта."""
        return f'{self.name}'
