from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AvatarUser


class CustomUserAdmin(UserAdmin):
    model = AvatarUser
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
            'is_staff', 'is_active', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
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


admin.site.register(AvatarUser, CustomUserAdmin)
