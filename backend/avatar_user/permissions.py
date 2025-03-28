"""Разрешения avatar_user."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс проверки авторства при методах изменения объектов."""

    def has_object_permission(self, request, _, obj):
        """Проверка авторства при методах изменения объектов."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
