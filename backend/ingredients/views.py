"""Представления ingredients."""
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import viewsets

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientFilter(FilterSet):
    """Фильтр ингредиентов по названию."""

    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        """Мета-информация фильтра ингредиентов."""

        model = Ingredient
        fields = ('name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
