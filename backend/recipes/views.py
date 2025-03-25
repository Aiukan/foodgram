"""Представления recipes."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Recipe."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
