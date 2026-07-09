from django.contrib import admin
from .models import UserBehaviorLog

@admin.register(UserBehaviorLog)
class UserBehaviorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'action', 'timestamp']
    list_filter = ['action']
