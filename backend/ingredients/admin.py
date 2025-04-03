"""Админ-зона приложения ingredients."""
from django.contrib import admin

from ingredients.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    """Модель админ-зоны Ingredient."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_display_links = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
