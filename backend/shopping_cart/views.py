from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import ShoppingCart
from recipes.models import Recipe
from .serializers import ShoppingCartSerializer
from rest_framework.views import APIView


class ShoppingCartView(APIView):
    """Вьюсет модели ShoppingCart."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        """Добавляет рецепт в корзину."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {"error": "Рецепт уже в корзине."},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShoppingCartSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """Удаление рецепта из списка покупок."""
        recipe = get_object_or_404(Recipe, id=id)
        cart_entry = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if not cart_entry.exists():
            return Response(
                {"error": "Рецепт не обнаружен в списке покупок."},
                status=status.HTTP_404_NOT_FOUND
            )
        cart_entry.delete()
        return Response(
            {"message": "Рецепт успешно удален из списка покупок."},
            status=status.HTTP_204_NO_CONTENT
        )
