"""Сериализаторы avatar_user."""
from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from api.serializers import Base64ImageField
from subscriptions.models import Subscription

User = get_user_model()


class AvatarUserCreationSerializer(UserCreateSerializer):
    """Сериализатор AvatarUser для создания пользователей."""

    first_name = serializers.CharField(
        required=True, max_length=settings.MAX_FIRST_NAME_LENGTH
    )
    last_name = serializers.CharField(
        required=True, max_length=settings.MAX_LAST_NAME_LENGTH
    )

    class Meta(UserCreateSerializer.Meta):
        """Мета-информация сериализатора AvatarUser."""

        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password'
        )

    def validate_first_name(self, value):
        """Проверка, что first_name не пустое."""
        if not value.strip():
            raise serializers.ValidationError('Введите имя.')
        return value

    def validate_last_name(self, value):
        """Проверка, что last_name не пустое."""
        if not value.strip():
            raise serializers.ValidationError('Введите фамилию.')
        return value


class AvatarUserSerializer(UserCreateSerializer):
    """Сериализатор AvatarUser для отображения пользователей."""

    avatar = Base64ImageField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        """Мета-информация сериализатора AvatarUser."""

        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password', 'avatar',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Получение информации о подписке на пользователя."""
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return Subscription.objects.filter(
                user_from=request.user,
                user_to=obj
            ).exists()
        return False


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta:
        """Метаинформация сериализатора аватара пользователя."""

        model = User
        fields = ('avatar',)
