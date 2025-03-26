from rest_framework import serializers
from .models import Recipe
from api.serializers import Base64ImageField


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор Recipe при создании ShoppingCart."""

    image = Base64ImageField()

    class Meta:
        """Мета-информация сериализатора добавления рецепта."""

        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
