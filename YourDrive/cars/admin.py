from django.contrib import admin
from .models import Brand, Car


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')
    list_filter = ('country',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model_year', 'price', 'fuel_type', 'transmission', 'is_available')
    list_filter = ('brand', 'fuel_type', 'transmission', 'is_available', 'model_year')
    search_fields = ('name', 'brand__name', 'description')
    list_editable = ('is_available',)
    fieldsets = (
        ('Basic Info', {'fields': ('brand', 'name', 'model_year', 'price', 'color', 'image')}),
        ('Specifications', {'fields': ('fuel_type', 'transmission', 'seats', 'mileage', 'engine_cc', 'horsepower')}),
        ('Additional', {'fields': ('description', 'features', 'is_available')}),
    )
