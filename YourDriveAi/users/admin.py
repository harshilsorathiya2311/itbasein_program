from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'budget', 'city', 'phone']
    search_fields = ['user__username', 'city']
