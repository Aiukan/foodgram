"""Админ-зона приложения recipes."""
from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    """Вложенная модель админ-зоны RecipeIngredient."""

    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """Модель админ-зоны Recipe."""

    list_display = (
        'name', 'get_author_username', 'date_created', 'favorite_count'
    )
    search_fields = ('name', 'author__username')
    list_filter = ('tags', 'date_created', 'cooking_time')
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('favorite_count',)

    @admin.display(description='Автор')
    def get_author_username(self, obj):
        return obj.author.username

    @admin.display(description='Добавлено в избранное')
    def favorite_count(self, obj):
        return obj.farovite_users.count()


admin.site.register(Recipe, RecipeAdmin)
