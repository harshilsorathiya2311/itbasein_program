from django.contrib import admin
from .models import Brand, Car

class CarInline(admin.TabularInline):
    model = Car
    fields = ['name', 'price', 'fuel_type', 'transmission']
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
    list_display = ['name', 'brand', 'price', 'fuel_type', 'transmission', 'mileage', 'seating_capacity', 'is_available']
    list_filter = ['brand', 'fuel_type', 'transmission', 'is_available']
    search_fields = ['name', 'brand__name', 'description']
    list_editable = ['is_available']
    list_per_page = 25
    fieldsets = (
        ('Basic Info', {
            'fields': ('brand', 'name', 'price', 'description')
        }),
        ('Specifications', {
            'fields': ('fuel_type', 'transmission', 'mileage', 'seating_capacity', 'engine_cc', 'power')
        }),
        ('Media & Status', {
            'fields': ('image', 'is_available')
        }),
    )
