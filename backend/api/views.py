"""Представления API проекта."""
import django_filters
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Exists, F, OuterRef, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import RecipePagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (AvatarSerializer, FavoriteCreateSerializer,
                             IngredientSerializer,
                             RecipeCreateUpdateSerializer,
                             RecipeRetrieveSerializer,
                             ShoppingCartCreateSerializer,
                             SubscriptionCreateSerializer,
                             SubscriptionsSerializer, TagSerializer)
from favorite.models import Favorite
from foodgram_backend.constants import INGREDIENT_FORMAT
from ingredients.models import Ingredient
from recipes.models import Recipe
from shopping_cart.models import ShoppingCart
from subscriptions.models import Subscription
from tags.models import Tag

User = get_user_model()


class UserViewSet(UserViewSet):
    """Вьюсет для пользователей Foodgram."""

    @action(
        detail=False, methods=['put'],
        url_path='me/avatar', permission_classes=[IsAuthenticated]
    )
    def update_avatar(self, request):
        """Обновление аватара пользователя."""
        user = request.user
        serializer = AvatarSerializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @update_avatar.mapping.delete
    def delete_avatar(self, request):
        """Удаление аватара пользователя."""
        user = request.user
        if not user.avatar:
            return Response(
                {"detail": "Нет аватара для удаления."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post'], url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def update_subscribe(self, request, id=None):
        """Подписка на пользователя."""
        user_to = get_object_or_404(User, id=id)
        user_from = request.user
        serializer = SubscriptionCreateSerializer(
            data={'user_from': user_from.id, 'user_to': user_to.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @update_subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Отписка от пользователя."""
        user_to = get_object_or_404(User, id=id)
        user_from = request.user
        deleted_count, _ = Subscription.objects.filter(
            user_from=user_from, user_to=user_to
        ).delete()
        if not deleted_count:
            return Response(
                {'error': 'Вы не подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Получение списка всех подписок текущего пользователя."""
        user = request.user
        subscribed_users = User.objects.filter(
            Exists(Subscription.objects.filter(
                user_from=user, user_to=OuterRef('id')
            ))
        )
        page = self.paginate_queryset(subscribed_users)
        serializer = SubscriptionsSerializer(
            page if page is not None else subscribed_users,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        """Ограничение users/me/ только для GET-запросов."""
        return super().me(request, *args, **kwargs)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Recipe."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_queryset(self):
        """Оптимизация получения кверисета."""
        user = (
            self.request.user if self.request.user.is_authenticated else None
        )
        return (
            Recipe.objects.select_related('author').annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe=OuterRef('id')
                )),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=user, recipe=OuterRef('id')
                ))
            ).prefetch_related('ingredients__ingredient', 'tags')
        )

    def get_serializer_class(self):
        """Разделение сериализаторов на получение и обновление данных."""
        return (
            RecipeRetrieveSerializer if self.action in ['list', 'retrieve']
            else RecipeCreateUpdateSerializer
        )

    @action(
        detail=True, methods=['post'], url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def update_favorite(self, request, pk=None):
        """Добавление в избранное."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = FavoriteCreateSerializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @update_favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление из избранного."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        deleted_count, _ = Favorite.objects.filter(
            user=user, recipe=recipe
        ).delete()
        if not deleted_count:
            return Response(
                {"error": "Рецепт не обнаружен в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post'], url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def update_shopping_cart(self, request, pk=None):
        """Добавление рецепта в списка покупок."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = ShoppingCartCreateSerializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @update_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из списка покупок."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        deleted_count, _ = ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).delete()
        if not deleted_count:
            return Response(
                {"error": "Рецепт не обнаружен в списке покупок."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Скачивание списка покупок текущего пользователя."""
        user = request.user
        ingredients = (
            Recipe.objects.filter(shopping_cart__user=user)
            .prefetch_related('ingredients__ingredient')
            .values(
                ingredient_name=F('ingredients__ingredient__name'),
                unit=F('ingredients__ingredient__measurement_unit')
            )
            .annotate(total_amount=Sum('ingredients__amount'))
            .order_by('ingredient_name')
        )
        lines = [
            INGREDIENT_FORMAT.format(
                f"{item['ingredient_name']} ({item['unit']})",
                item['total_amount']
            )
            for item in ingredients
        ]
        content = 'Полный список ингредиентов:\n' + ';\n'.join(lines) + '.'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        """Представление для получения короткой ссылки на рецепт."""
        recipe = self.get_object()
        short_url = request.build_absolute_uri(f'/s/{recipe.short_code}/')
        if settings.SECURE_PROXY_SSL_HEADER:
            short_url = short_url.replace("http://", "https://")
        return Response({'short-link': short_url})


@api_view(('GET',))
def short_recipe_url(request, encoded):
    """Представление для перехода на страницу рецепта по короткой ссылке."""
    recipe = get_object_or_404(Recipe, short_code=encoded)
    recipe_url = f'/recipes/{recipe.id}/'
    return HttpResponseRedirect(recipe_url)
