"""Сериализаторы recipes."""
from rest_framework import serializers

from api.serializers import Base64ImageField
from avatar_user.serializers import AvatarUserSerializer
from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer

from .models import Recipe, RecipeIngredient


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
        required=True,
    )
    amount = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        """Мета-информация сериализатора создания RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор получения RecipeIngredient."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        """Мета-информация сериализатора получения RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецептов."""

    ingredients = RecipeIngredientCreateSerializer(
        many=True, required=True, allow_empty=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True, allow_empty=False
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'name', 'text', 'image',
            'ingredients', 'tags', 'cooking_time'
        )

    def validate_ingredients(self, value):
        """Проверка уникальности ингредиентов."""
        seen = set()
        for obj in value:
            ingredient_id = obj['ingredient']['id']
            if ingredient_id in seen:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными.'
                )
            seen.add(ingredient_id)
        return value

    def validate_tags(self, value):
        """Проверка уникальности тегов."""
        unique_tags = set(value)
        if len(unique_tags) != len(value):
            raise serializers.ValidationError('Теги должны быть уникальными.')
        return value

    def validate(self, data):
        """Общая валидация полей ingredients и tags."""
        if 'ingredients' not in data or not data['ingredients']:
            raise serializers.ValidationError(
                {'ingredients': 'Необходимо добавить хотя бы один ингредиент.'}
            )
        if 'tags' not in data or not data['tags']:
            raise serializers.ValidationError(
                {'tags': 'Необходимо выбрать хотя бы один тег.'}
            )
        return data

    def create(self, validated_data):
        """Переопределение метода create.

        Добавление пользователя данной сессии к данным и
        раздельная обработка ингредиентов.
        """
        ingredients_data = validated_data.pop('ingredients')
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['author'] = request.user
        recipe = super().create(validated_data)
        self._create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Переопределение метода update.

        Раздельная обработка ингредиентов.
        """
        ingredients_data = validated_data.pop('ingredients', [])
        instance = super().update(instance, validated_data)
        instance.ingredients.all().delete()
        self._create_ingredients(instance, ingredients_data)
        return instance

    def _create_ingredients(self, recipe, ingredients_data):
        """Внутренний метод для обработки ингредиентов."""
        ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(ingredients)


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор с полной информацией о рецепте."""

    ingredients = RecipeIngredientRetrieveSerializer(many=True)
    author = AvatarUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.BooleanField()
    is_favorited = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'text', 'image', 'ingredients', 'tags',
            'cooking_time', 'author', 'is_in_shopping_cart', 'is_favorited'
        )


class ShortCardRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор короткого описания Recipe."""

    image = Base64ImageField()

    class Meta:
        """Мета-информация сериализатора короткого описания Recipe."""

        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
