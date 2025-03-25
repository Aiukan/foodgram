"""Сериализаторы recipes."""
from rest_framework import serializers

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор класса Recipe."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Мета-информация сериализатора Recipe."""

        fields = (
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'author'
        )
        model = Recipe
