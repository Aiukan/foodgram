"""URL конфигурация recipes."""
from django.urls import path
from .views import short_recipe_url

app_name = 'recipes'

urlpatterns = [
    path(
        's/<encoded>/',
        short_recipe_url,
        name='short-recipe-url'
    ),
]
