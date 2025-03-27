"""Сериализаторы avatar_user."""

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.serializers import Base64ImageField
from subscriptions.models import Subscription

User = get_user_model()


class AvatarUserSerializer(UserCreateSerializer):
    """Сериализатор AvatarUser."""

    avatar = avatar = Base64ImageField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password', 'avatar',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return Subscription.objects.filter(
                user_from=request.user,
                user_to=obj
            ).exists()
        return False


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара пользователя."""
    avatar = Base64ImageField()

    class Meta:
        """Метаинформация сериализатора аватара пользователя."""

        model = User
        fields = ('avatar',)
