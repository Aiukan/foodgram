"""Сериализаторы tags."""
from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор класса Tag."""

    class Meta:
        """Мета-информация сериализатора Tag."""

        fields = ('id', 'name', 'slug')
        model = Tag
