"""Представления recipes."""
import base62
import django_filters
from avatar_user.permissions import IsAuthorOrReadOnly
from django.db.models import Exists, OuterRef
from django.http import (HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from favorite.models import Favorite
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from shopping_cart.models import ShoppingCart
from tags.models import Tag

from .models import Recipe
from .serializers import RecipeCreateUpdateSerializer, RecipeRetrieveSerializer


class RecipePagination(PageNumberPagination):
    """Класс пагинации для рецепта."""

    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 20

    def get_paginated_response(self, data):
        """Пагинация по страницам с параметром limit."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class RecipeFilter(django_filters.FilterSet):
    """Фильтр вьюсета RecipeViewSet."""

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
        conjoined=False,
    )
    author = django_filters.NumberFilter(field_name="author__id")
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited'
    )

    class Meta:
        """Мета-информация RecipeFilter."""

        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, _, value):
        """Фильтр проверки нахождения в избранном."""
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(
            Exists(Favorite.objects.filter(user=user, recipe=OuterRef('id')))
        ) if value else queryset.exclude(
            Exists(Favorite.objects.filter(user=user, recipe=OuterRef('id')))
        )

    def filter_is_in_shopping_cart(self, queryset, _, value):
        """Фильтр проверки нахождения в списке покупок."""
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(
            Exists(ShoppingCart.objects.filter(
                user=user, recipe=OuterRef('id')
            ))
        ) if value else queryset.exclude(
            Exists(ShoppingCart.objects.filter(
                user=user, recipe=OuterRef('id')
            ))
        )


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Recipe."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    queryset = Recipe.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_queryset(self):
        """Оптимизация получения кверисета."""
        user = (
            self.request.user
            if self.request and self.request.user.is_authenticated
            else None)
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
        if self.action in ['list', 'retrieve']:
            return RecipeRetrieveSerializer
        return RecipeCreateUpdateSerializer


@api_view(('GET',))
def get_short_recipe_url(request, id):
    """Представление для получения короткой ссылки на рецепт."""
    encoded_id = base62.encode(id)
    short_url = request.build_absolute_uri(f'/s/{encoded_id}')
    return JsonResponse({'short-link': short_url})


@api_view(('GET',))
def short_recipe_url(request, encoded):
    """Представление для перехода на страницу рецепта по короткой ссылке."""
    try:
        id = base62.decode(encoded)
    except ValueError:
        return HttpResponseNotFound('Введен некорректный код рецепта.')
    recipe_url = f'/recipes/{id}/'
    return HttpResponseRedirect(recipe_url)
