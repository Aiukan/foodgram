from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_created')
    search_fields = ('name', 'author')
    list_filter = ('tags', 'ingredients', 'date_created', 'cooking_time')


admin.site.register(Recipe, RecipeAdmin)
