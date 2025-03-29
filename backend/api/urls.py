"""URL эндпоинты API проекта foodgram_backend."""
from django.urls import include, path
from rest_framework import routers

from avatar_user.views import AvatarView, CustomUserViewSet
from favorite.views import FavoriteView
from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet, get_short_recipe_url
from shopping_cart.views import ShoppingCartView, download_shopping_cart
from subscriptions.views import SubscriptionListView, SubscriptionView
from tags.views import TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path(
        'users/me/',
        CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'}),
        name='user-me'
    ),
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping-cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscriptionView.as_view(),
        name='subscribtion-list'
    ),
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='subscribe'
    ),
    path(
        'users/<int:id>/subscribe/',
        get_short_recipe_url,
        name='get-short-recipe-url'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download-shopping-cart'
    ),
    path(
        'recipes/<int:id>/get-link/',
        get_short_recipe_url,
        name='get-short-recipe-url'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
