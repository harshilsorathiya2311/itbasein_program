from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPreference


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_admin', 'is_staff', 'date_joined')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'budget', 'is_admin')}),
    )


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_brand', 'preferred_fuel_type', 'min_budget', 'max_budget')
    list_filter = ('preferred_fuel_type', 'preferred_transmission')


admin.site.register(User, CustomUserAdmin)
