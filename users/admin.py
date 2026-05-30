from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'surname',
                    'phone', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'surname', 'phone')
    ordering = ('email',)
    readonly_fields = ('last_login',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('name', 'surname', 'avatar', 'phone', 'github_url', 'about')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2'),
        }),
    )
