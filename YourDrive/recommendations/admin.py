from django.contrib import admin
from .models import RecommendationLog, UserBehavior


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ml_algorithm', 'confidence_score', 'created_at')
    list_filter = ('ml_algorithm', 'created_at')
    search_fields = ('user__username',)


@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'car__name')
