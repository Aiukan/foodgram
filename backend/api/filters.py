"""Представления ingredients."""
import django_filters
from django_filters.rest_framework import CharFilter, FilterSet

from ingredients.models import Ingredient
from recipes.models import Recipe

BOOLEAN_CHOICES = (
    ('0', False),
    ('1', True),
)


class IngredientFilter(FilterSet):
    """Фильтр ингредиентов по названию."""

    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        """Мета-информация фильтра ингредиентов."""

        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр вьюсета RecipeViewSet."""

    tags = django_filters.AllValuesMultipleFilter(field_name="tags__slug")
    author = django_filters.NumberFilter(field_name="author__id")
    is_in_shopping_cart = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=lambda x: x == '1'
    )
    is_favorited = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=lambda x: x == '1'
    )

    class Meta:
        """Мета-информация RecipeFilter."""

        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')
