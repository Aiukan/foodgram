"""Модели subscriptions."""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

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
        constraints = (
            models.UniqueConstraint(
                fields=('user_from', 'user_to'),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~Q(user_from=models.F('user_to')),
                name='prevent_self_subscription'
            ),
        )

    def __str__(self):
        """Представление подписки."""
        return f'{self.user_from} подписан на {self.user_to}.'
