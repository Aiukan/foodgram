"""Модели subscriptions."""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки на пользователя."""

    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    class Meta:
        """Мета-информация Subscription."""

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user_from', 'user_to')

    def clean(self):
        """Запрещает подписку на самого себя."""
        if self.user_from == self.user_to:
            raise ValidationError(
                "Пользователь не может подписаться на самого себя!"
            )

    def save(self, *args, **kwargs):
        """Вызов clean перед сохранением."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Представление подписки."""
        return f'{self.user_from} подписан на {self.user_to}.'
