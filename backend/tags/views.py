"""Представления tags."""
from rest_framework import viewsets

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
