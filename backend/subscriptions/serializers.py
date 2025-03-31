"""Сериализаторы subscriptions."""
from avatar_user.serializers import AvatarUserSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe
from recipes.serializers import ShortCardRecipeSerializer
from rest_framework import serializers

User = get_user_model()


class SubscriptionsSerializer(AvatarUserSerializer):
    """Сериализатор подписок пользователя."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        """Мета-информация сериализатора подписок."""

        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password', 'avatar',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        """Получение нескольких последних рецептов пользователя."""
        request = self.context.get('request')
        recipes_limit = request.query_params.get(
            "recipes_limit", settings.DEFAULT_RECIPES_LIMIT
        )
        try:
            recipes_limit = int(recipes_limit)
        except ValueError:
            recipes_limit = settings.DEFAULT_RECIPES_LIMIT
        recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        return ShortCardRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Получение количества рецептов пользователя."""
        return Recipe.objects.filter(author=obj).count()
