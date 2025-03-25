"""Модели avatar_user."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class AvatarUser(AbstractUser):
    """Кастомная модель пользователя, поддерживающая изображения."""

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """Мета-информация модели AvatarUser."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)

    def __str__(self):
        """Строковое представление пользователя."""
        return self.email
