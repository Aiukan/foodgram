from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Favorite
from recipes.models import Recipe
from recipes.serializers import ShortCardRecipeSerializer
from rest_framework.views import APIView


class FavoriteView(APIView):
    """Вьюсет модели Favorite."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        """Добавляет рецепт в избранное."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {"error": "Рецепт уже в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = ShortCardRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """Удаление рецепта из избранного."""
        recipe = get_object_or_404(Recipe, id=id)
        favorite_entry = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if not favorite_entry.exists():
            return Response(
                {"error": "Рецепт не обнаружен в избранном."},
                status=status.HTTP_404_NOT_FOUND
            )
        favorite_entry.delete()
        return Response(
            {"message": "Рецепт успешно удален из избранного."},
            status=status.HTTP_204_NO_CONTENT
        )
