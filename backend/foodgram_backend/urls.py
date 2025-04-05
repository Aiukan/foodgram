"""URL конфигурация foodgram_backend."""
from django.contrib import admin
from django.urls import include, path

from api.views import short_recipe_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('s/<encoded>/', short_recipe_url, name='short-recipe-url'),
]
