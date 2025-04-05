"""Модели recipes."""
import random
import string

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from foodgram_backend.constants import (AMOUNT_MAX_ERROR, AMOUNT_MIN_ERROR,
                                        COOKING_TIME_MAX,
                                        COOKING_TIME_MAX_ERROR,
                                        COOKING_TIME_MIN,
                                        COOKING_TIME_MIN_ERROR,
                                        INGREDIENT_AMOUNT_MAX,
                                        INGREDIENT_AMOUNT_MIN,
                                        RECIPE_NAME_MAX_LENGTH,
                                        SHORT_CODE_MAX_LENGTH)
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class RecipeIngredient(models.Model):
    """Связь ингредиентов и рецептов."""

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
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinValueValidator(
                INGREDIENT_AMOUNT_MIN, message=AMOUNT_MIN_ERROR
            ),
            validators.MaxValueValidator(
                INGREDIENT_AMOUNT_MAX, message=AMOUNT_MAX_ERROR
            ),
        )
    )

    class Meta:
        """Мета-информация RecipeIngredient."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            ),
        )
        ordering = ('ingredient', 'recipe')

    def __str__(self):
        """Строковое представление RecipeIngredient."""
        return f'{self.recipe} - {self.ingredient} ({self.amount})'


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH, unique=True, verbose_name='Название'
    )
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            validators.MinValueValidator(
                COOKING_TIME_MIN, message=COOKING_TIME_MIN_ERROR
            ),
            validators.MaxValueValidator(
                COOKING_TIME_MAX, message=COOKING_TIME_MAX_ERROR
            ),
        )
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор'
    )
    short_code = models.CharField(
        max_length=SHORT_CODE_MAX_LENGTH, unique=True,
        blank=True, null=True, verbose_name='Короткая ссылка'
    )

    class Meta:
        """Мета-информация Recipe."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date_created', 'name')

    def __str__(self):
        """Строковое представление рецепта."""
        return f'Рецепт {self.name}'

    def generate_short_code(self):
        """Генерация уникального короткого кода для рецепта."""
        length = SHORT_CODE_MAX_LENGTH
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(length))
        return short_code

    def save(self, *args, **kwargs):
        """Добавление короткого кода только при создании рецепта."""
        if not self.short_code:
            while True:
                short_code = self.generate_short_code()
                if not Recipe.objects.filter(short_code=short_code).exists():
                    self.short_code = short_code
                    break
        super().save(*args, **kwargs)
