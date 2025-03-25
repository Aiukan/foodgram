"""Сериализаторы avatar_user."""

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.serializers import Base64ImageField

User = get_user_model()


class AvatarUserCreateSerializer(UserCreateSerializer):
    """Сериализатор AvatarUser."""

    avatar = avatar = Base64ImageField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password', 'avatar'
        )


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара пользователя."""
    avatar = Base64ImageField()

    class Meta:
        """Метаинформация сериализатора аватара пользователя."""

        model = User
        fields = ('avatar',)
