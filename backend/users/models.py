"""Модели users."""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram_backend.constants import (MAX_EMAIL_LENGTH,
                                        MAX_FIRST_NAME_LENGTH,
                                        MAX_LAST_NAME_LENGTH,
                                        MAX_USERNAME_LENGTH)


class User(AbstractUser):
    """Модель пользователя, поддерживающая изображения."""

    email = models.EmailField(
        unique=True, verbose_name='Почта',
        max_length=MAX_EMAIL_LENGTH
    )
    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        verbose_name="Имя пользователя",
        help_text="Уникальное имя пользователя, используемое для входа.",
        validators=(UnicodeUsernameValidator(),)
    )
    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        verbose_name="Имя",
        help_text="Настоящее имя пользователя."
    )
    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя."
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True,
        default=None, verbose_name='Аватар'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        """Мета-информация модели User."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name', 'first_name')

    def __str__(self):
        """Строковое представление пользователя."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return 'Пользователь ' + (
            f'{full_name} ({self.email})' if full_name else self.email
        )
