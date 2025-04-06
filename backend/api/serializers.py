"""Сериализаторы API проекта."""
import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from favorite.models import Favorite
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
from shopping_cart.models import ShoppingCart
from subscriptions.models import Subscription
from tags.models import Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Класс представления изображения в формате Base64."""

    def to_internal_value(self, data):
        """Перевод изображений из формата Base64."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

    def to_representation(self, value):
        """Возвращает абсолютный URL изображения."""
        if not value:
            return None
        request = self.context.get("request")
        image_url = value.url
        if request is not None:
            return request.build_absolute_uri(image_url)
        return image_url


class UserSerializer(ModelSerializer):
    """Сериализатор User для отображения пользователей."""

    avatar = Base64ImageField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Мета-информация сериализатора User."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'avatar', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Получение информации о подписке на пользователя."""
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and Subscription.objects.filter(
                user_from=request.user, user_to=obj
            ).exists()
        )


class AvatarSerializer(ModelSerializer):
    """Сериализатор аватара пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta:
        """Метаинформация сериализатора аватара пользователя."""

        model = User
        fields = ('avatar',)

    def validate(self, data):
        """Проверка наличия и содержимого поля avatar."""
        if not self.initial_data.get('avatar'):
            raise serializers.ValidationError({
                'avatar': 'Поле "avatar" обязательно и не может быть пустым.'
            })
        return data


class FavoriteCreateSerializer(ModelSerializer):
    """Сериализатор для добавления в избранное."""

    class Meta:
        """Мета-информация сериализатора для добавления в избранное."""

        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        """Валидация добавления в избранное."""
        user = data.get('user')
        recipe = data.get('recipe')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("Рецепт уже в избранном.")
        return data

    def to_representation(self, instance):
        """После добавления в избранное возвращается карточка рецепта."""
        return ShortCardRecipeSerializer(
            instance.recipe,
            context=self.context
        ).data


class ShoppingCartCreateSerializer(ModelSerializer):
    """Сериализатор для добавления в список покупок."""

    class Meta:
        """Мета-информация сериализатора добавления в список покупок."""

        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        """Валидация добавления в список покупок."""
        user = data.get('user')
        recipe = data.get('recipe')
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("Рецепт уже в списке покупок.")
        return data

    def to_representation(self, instance):
        """После добавления в список покупок возвращается карточка рецепта."""
        return ShortCardRecipeSerializer(
            instance.recipe,
            context=self.context
        ).data


class IngredientSerializer(ModelSerializer):
    """Сериализатор класса Ingredient."""

    class Meta:
        """Мета-информация сериализатора Ingredient."""

        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(ModelSerializer):
    """Сериализатор класса Tag."""

    class Meta:
        """Мета-информация сериализатора Tag."""

        fields = ('id', 'name', 'slug')
        model = Tag


class SubscriptionsSerializer(UserSerializer):
    """Сериализатор подписок пользователя."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Мета-информация сериализатора подписок."""

        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'avatar',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        """Получение рецептов пользователя (с ограничением)."""
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        try:
            recipes = recipes[:int(request.query_params.get('recipes_limit'))]
        except TypeError:
            pass
        return ShortCardRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Количество рецептов пользователя."""
        return Recipe.objects.filter(author=obj).count()


class SubscriptionCreateSerializer(ModelSerializer):
    """Сериализатор для подписки на пользователя."""

    class Meta:
        """Мета-информация сериализатора для подписки на пользователя."""

        model = Subscription
        fields = ('user_from', 'user_to')

    def validate(self, data):
        """Проверка на самоподписку и повторную подписку."""
        user_from = data.get('user_from')
        user_to = data.get('user_to')
        if user_from == user_to:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        if Subscription.objects.filter(
            user_from=user_from, user_to=user_to
        ).exists():
            raise serializers.ValidationError('Подписка уже существует.')
        return data

    def to_representation(self, instance):
        """Вернуть данные пользователя, на которого подписались."""
        return SubscriptionsSerializer(
            instance.user_to,
            context=self.context
        ).data


class RecipeIngredientCreateSerializer(ModelSerializer):
    """Сериализатор создания RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
        required=True,
    )

    class Meta:
        """Мета-информация сериализатора создания RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientRetrieveSerializer(ModelSerializer):
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


class RecipeCreateUpdateSerializer(ModelSerializer):
    """Сериализатор для создания и изменения рецептов."""

    ingredients = RecipeIngredientCreateSerializer(
        many=True, required=True, allow_empty=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True, allow_empty=False
    )
    image = Base64ImageField(required=True)

    class Meta:
        """Мета-информация сериализатора для обновления рецептов."""

        model = Recipe
        fields = (
            'name', 'text', 'image', 'ingredients', 'tags', 'cooking_time'
        )

    def validate(self, data):
        """Проверяет, что в рецепте есть уникальные ингредиенты и теги."""
        ingredients = data.get('ingredients', [])
        tags = data.get('tags', [])
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Необходимо добавить хотя бы один ингредиент.'}
            )
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Необходимо выбрать хотя бы один тег.'}
            )
        seen_ingredients = set()
        for obj in ingredients:
            ingredient_id = obj['ingredient']['id']
            if ingredient_id in seen_ingredients:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиенты должны быть уникальными.'}
                )
            seen_ingredients.add(ingredient_id)
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                {'tags': 'Теги должны быть уникальными.'}
            )
        return data

    def create(self, validated_data):
        """Создание рецепта с обработкой ингредиентов."""
        ingredients_data = validated_data.pop('ingredients')
        validated_data['author'] = self.context['request'].user
        recipe = super().create(validated_data)
        self._create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Обновление рецепта с обработкой ингредиентов."""
        ingredients_data = validated_data.pop('ingredients', [])
        instance = super().update(instance, validated_data)
        instance.ingredients.all().delete()
        self._create_ingredients(instance, ingredients_data)
        return instance

    @staticmethod
    def _create_ingredients(recipe, ingredients_data):
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

    def to_representation(self, instance):
        """Возвращает представление рецепта после создания/обновления."""
        instance = self.context.get('view').get_queryset().get(pk=instance.pk)
        return RecipeRetrieveSerializer(instance, context=self.context).data


class RecipeRetrieveSerializer(ModelSerializer):
    """Сериализатор с полной информацией о рецепте."""

    ingredients = RecipeIngredientRetrieveSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        """Мета-информация сериализатора с полной информацией о рецепте."""

        model = Recipe
        fields = (
            'id', 'name', 'text', 'image', 'ingredients', 'tags',
            'cooking_time', 'author', 'is_in_shopping_cart', 'is_favorited'
        )


class ShortCardRecipeSerializer(ModelSerializer):
    """Сериализатор короткого описания Recipe."""

    image = Base64ImageField()

    class Meta:
        """Мета-информация сериализатора короткого описания Recipe."""

        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
