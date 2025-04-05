"""Админ-зона приложения recipes."""
from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    """Вложенная модель админ-зоны RecipeIngredient."""

    min_num = 1
    model = RecipeIngredient
    extra = 1

    def get_queryset(self, request):
        """Оптимизация для снижения количества запросов."""
        qs = super().get_queryset(request)
        return qs.select_related('ingredient', 'recipe')


class RecipeAdmin(admin.ModelAdmin):
    """Модель админ-зоны Recipe."""

    list_display = (
        'name', 'get_author_username', 'date_created'
    )
    list_select_related = ('author',)
    search_fields = ('name', 'author__username')
    list_filter = ('tags', 'date_created', 'cooking_time')
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('favorite_count',)

    @admin.display(description='Автор')
    def get_author_username(self, obj):
        """Получение имени пользователя автора."""
        return obj.author.username

    @admin.display(description='Добавлено в избранное')
    def favorite_count(self, obj):
        """Количество добавлений рецепта в избранное."""
        return obj.favorited_by.count()


admin.site.register(Recipe, RecipeAdmin)
