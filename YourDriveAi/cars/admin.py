from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Car

class CarInline(admin.TabularInline):
    model = Car
    fields = ['name', 'price', 'fuel_type', 'transmission', 'body_type']
    extra = 1
    show_change_link = True

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year', 'car_count']
    search_fields = ['name']
    inlines = [CarInline]

    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = 'Cars'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'name', 'brand', 'price', 'fuel_type', 'transmission', 'body_type', 'safety_rating', 'seating_capacity', 'is_available']
    list_filter = ['brand', 'fuel_type', 'transmission', 'body_type', 'is_available']
    search_fields = ['name', 'brand__name', 'description']
    list_editable = ['is_available']
    list_per_page = 25
    list_select_related = ['brand']
    fieldsets = (
        ('Basic Info', {
            'fields': ('brand', 'name', 'price', 'description')
        }),
        ('Specifications', {
            'fields': ('fuel_type', 'transmission', 'mileage', 'seating_capacity', 'body_type', 'engine_cc', 'power')
        }),
        ('Safety & Status', {
            'fields': ('safety_rating', 'is_available')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
    )
    readonly_fields = ['image_preview']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:35px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<span style="color:#999">No img</span>')
    thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px;max-height:200px;border-radius:8px;">', obj.image.url)
        return 'No image uploaded'
    image_preview.short_description = 'Image Preview'
