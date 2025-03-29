"""Представления avatar_user."""
from django.core.files.storage import default_storage
from djoser.views import UserViewSet
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AvatarSerializer


class AvatarView(views.APIView):
    """Представления для операций над аватаром модели AvatarUser."""

    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        """Переопределние метода put для загрузки аватара пользователя."""
        if 'avatar' not in request.data:
            return Response(
                {"detail": 'Отсутствует изображение.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AvatarSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if request.user.avatar:
                default_storage.delete(request.user.avatar.path)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """Переопределние метода delete для удаления аватара пользователя."""
        user = request.user
        if user.avatar:
            default_storage.delete(user.avatar.path)
            user.avatar = None
            user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для ограничения users/me/ для анонимных пользователей."""

    def me(self, request):
        """Проверка авторизации перед выполнением users/me/."""
        if not request.user or request.user.is_anonymous:
            return Response(
                {"detail": 'Страница ограничена для анонимных пользователей.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().me(request)
