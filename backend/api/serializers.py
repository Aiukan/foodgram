"""Общие сериализаторы для API foodgram_backend."""
import base64

from rest_framework import serializers
from django.core.files.base import ContentFile


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
