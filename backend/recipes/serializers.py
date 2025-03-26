"""Сериализаторы recipes."""
from rest_framework import serializers

from ingredients.models import Ingredient
from .models import Recipe, RecipeIngredient
from avatar_user.serializers import AvatarUserSerializer
from tags.serializers import TagSerializer
from api.serializers import Base64ImageField
from shopping_cart.models import ShoppingCart


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор класса RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        """Мета-информация сериализатора RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор класса Recipe."""

    ingredients = RecipeIngredientSerializer(many=True)
    author = AvatarUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        """Мета-информация сериализатора Recipe."""

        fields = (
            'id',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'author',
            'image',
            'is_in_shopping_cart'
        )
        read_only_fields = ('id',)
        model = Recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['author'] = request.user
        recipe = super().create(validated_data)
        self._create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        instance = super().update(instance, validated_data)
        instance.ingredients.all().delete()
        self._create_ingredients(instance, ingredients_data)
        return instance

    def _create_ingredients(self, recipe, ingredients_data):
        ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(ingredients)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                recipe=obj,
                user=request.user
            ).exists()
        return False
