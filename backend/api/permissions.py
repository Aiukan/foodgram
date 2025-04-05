"""Разрешения API проекта."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс проверки авторства при изменении объектов."""

    def has_object_permission(self, request, _, obj):
        """Проверка авторства при изменении объектов."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
