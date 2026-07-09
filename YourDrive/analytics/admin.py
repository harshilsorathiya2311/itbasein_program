from django.contrib import admin
from .models import PageView

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'url', 'user', 'created_at']
    list_filter = ['page_name', 'created_at']
