"""URL эндпоинты API проекта foodgram_backend."""

from django.urls import include, path
from rest_framework import routers

from tags.views import TagViewSet
from recipes.views import RecipeViewSet
from ingredients.views import IngredientViewSet
from avatar_user.views import AvatarView
from shopping_cart.views import ShoppingCartView


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping-cart'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
