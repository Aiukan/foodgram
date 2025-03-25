"""Сериализаторы ingredients."""
from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор класса Ingredient."""

    class Meta:
        """Мета-информация сериализатора Ingredient."""

        fields = ('name', 'measurement_unit')
        model = Ingredient
