"""Админ-зона приложения tags."""
from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    """Модель админ-зоны Tag."""

    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(Tag, TagAdmin)
