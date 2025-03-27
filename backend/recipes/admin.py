from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_created')
    search_fields = ('name', 'author__username')
    list_filter = ('tags', 'date_created', 'cooking_time')
    inlines = (RecipeIngredientInline,)


admin.site.register(Recipe, RecipeAdmin)
