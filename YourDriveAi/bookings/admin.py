from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Booking, Review


@admin.action(description='Approve selected bookings')
def approve_bookings(modeladmin, request, queryset):
    updated = queryset.update(status='Approved')
    messages.success(request, f'{updated} booking(s) approved.')


@admin.action(description='Reject selected bookings')
def reject_bookings(modeladmin, request, queryset):
    updated = queryset.update(status='Rejected')
    messages.success(request, f'{updated} booking(s) rejected.')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_name', 'user_email', 'car_name', 'booking_date',
        'booking_time', 'phone_number', 'status_colored', 'created_at'
    ]
    list_filter = ['status', 'booking_date', 'car__brand']
    search_fields = ['user__username', 'user__email', 'car__name', 'phone_number']
    list_per_page = 25
    actions = [approve_bookings, reject_bookings]
    readonly_fields = ['created_at', 'updated_at', 'status_changed_at']

    fieldsets = (
        ('Customer Info', {
            'fields': ('user', 'car', 'phone_number', 'address')
        }),
        ('Booking Details', {
            'fields': ('booking_date', 'booking_time', 'dealership', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'status_changed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def user_name(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    user_name.short_description = 'User'
    user_name.admin_order_field = 'user__username'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def car_name(self, obj):
        url = reverse('admin:cars_car_change', args=[obj.car_id])
        return format_html('<a href="{}">{}</a>', url, obj.car.name)
    car_name.short_description = 'Car'
    car_name.admin_order_field = 'car__name'

    def status_colored(self, obj):
        colors = {
            'Pending': 'orange',
            'Approved': 'green',
            'Rejected': 'red',
            'Completed': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.status
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'car__brand')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rating', 'created_at']
    list_filter = ['rating', 'car__brand']
    search_fields = ['user__username', 'car__name', 'comment']
