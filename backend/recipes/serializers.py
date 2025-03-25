"""Сериализаторы recipes."""
from rest_framework import serializers

from .models import Recipe, RecipeIngredient
from api.serializers import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор класса RecipeIngredient."""

    class Meta:
        """Мета-информация сериализатора RecipeIngredient."""

        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор класса Recipe."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    image = Base64ImageField()

    class Meta:
        """Мета-информация сериализатора Recipe."""

        fields = (
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'author',
            'image'
        )
        model = Recipe
