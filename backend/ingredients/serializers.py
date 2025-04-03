"""Сериализаторы ingredients."""
from rest_framework import serializers

from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор класса Ingredient."""

    class Meta:
        """Мета-информация сериализатора Ingredient."""

        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
