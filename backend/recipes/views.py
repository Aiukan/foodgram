"""Представления recipes."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe
from tags.models import Tag
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RecipeSerializer
from rest_framework.decorators import api_view
import base62
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.db.models import Exists, OuterRef
from favorite.models import Favorite
from shopping_cart.models import ShoppingCart


class RecipeFilter(django_filters.FilterSet):
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
        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, _, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(
            Exists(Favorite.objects.filter(user=user, recipe=OuterRef('id')))
        ) if value else queryset.exclude(
            Exists(Favorite.objects.filter(user=user, recipe=OuterRef('id')))
        )

    def filter_is_in_shopping_cart(self, queryset, _, value):
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

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter


@api_view(('GET',))
def get_short_recipe_url(request, id):
    encoded_id = base62.encode(id)
    short_url = request.build_absolute_uri(f'/s/{encoded_id}')
    return JsonResponse({'short-link': short_url})


@api_view(('GET',))
def short_recipe_url(request, encoded):
    try:
        id = base62.decode(encoded)
    except ValueError:
        return HttpResponseNotFound('Введен некорректный код рецепта.')
    recipe_url = f'/recipes/{id}/'
    return HttpResponseRedirect(recipe_url)
