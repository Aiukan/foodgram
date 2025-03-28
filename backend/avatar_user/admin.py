from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AvatarUser
from shopping_cart.models import ShoppingCart
from favorite.models import Favorite
from subscriptions.models import Subscription


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = 'user_from'
    extra = 1


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class CustomUserAdmin(UserAdmin):
    model = AvatarUser
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
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


admin.site.register(AvatarUser, CustomUserAdmin)
