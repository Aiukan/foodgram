"""Админ-зона приложения avatar_user."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from favorite.models import Favorite
from shopping_cart.models import ShoppingCart
from subscriptions.models import Subscription

from .models import AvatarUser


class SubscriptionInline(admin.TabularInline):
    """Вложенная модель админ-зоны Subscription."""

    model = Subscription
    fk_name = 'user_from'
    extra = 1

    def get_queryset(self, request):
        """Оптимизация для снижения количества запросов."""
        qs = super().get_queryset(request)
        return qs.select_related('user_from', 'user_to')


class FavoriteInline(admin.TabularInline):
    """Вложенная модель админ-зоны Favorite."""

    model = Favorite
    extra = 1

    def get_queryset(self, request):
        """Оптимизация для снижения количества запросов."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'recipe')


class ShoppingCartInline(admin.TabularInline):
    """Вложенная модель админ-зоны ShoppingCart."""

    model = ShoppingCart
    extra = 1

    def get_queryset(self, request):
        """Оптимизация для снижения количества запросов."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'recipe')


class AvatarUserAdmin(UserAdmin):
    """Модель админ-зоны AvatarUser."""

    model = AvatarUser
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'avatar')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права', {'fields': (
            'is_staff', 'is_active', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'first_name', 'last_name',
                    'password1', 'password2', 'is_staff', 'is_active'
                )
            }
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('id',)
    list_display_links = ('id', 'username')
    inlines = (SubscriptionInline, FavoriteInline, ShoppingCartInline)


admin.site.register(AvatarUser, AvatarUserAdmin)
