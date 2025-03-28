"""Представления shopping_cart."""
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import ShortCardRecipeSerializer

from .models import ShoppingCart

INGREDIENT_FORMAT = '  * {} - {}'


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
        serializer = ShortCardRecipeSerializer(
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


@api_view(('GET',))
def download_shopping_cart(request):
    """Представление для загрузки файла списка покупок."""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Пользователь не авторизован."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    user = request.user
    total_ingredients = defaultdict(int)
    recipes = Recipe.objects.filter(shopping_cart__user=user)
    for recipe in recipes:
        for recipe_ingredient in recipe.ingredients.all():
            total_ingredients[recipe_ingredient.ingredient.name] += (
                recipe_ingredient.amount
            )
    point_format_entries = [
        INGREDIENT_FORMAT.format(ingredient, amount)
        for ingredient, amount in total_ingredients.items()
    ]
    content = 'Полный список ингредиентов:\n'
    content += '\n'.join(point_format_entries)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="sample.txt"'
    return response
