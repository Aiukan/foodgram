"""Представления recipes."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe
from tags.models import Tag
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RecipeSerializer


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
        conjoined=False,
    )
    author = django_filters.NumberFilter(field_name="author__id")

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Recipe."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
