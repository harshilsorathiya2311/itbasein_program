from django.contrib import admin
from .models import TestDriveBooking


@admin.register(TestDriveBooking)
class TestDriveBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'booking_date', 'booking_time', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'car__brand')
    search_fields = ('user__username', 'car__name', 'car__brand__name')
    list_editable = ('status',)
    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, f'{queryset.count()} bookings approved.')
    approve_bookings.short_description = 'Approve selected bookings'

    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, f'{queryset.count()} bookings rejected.')
    reject_bookings.short_description = 'Reject selected bookings'

    fieldsets = (
        ('Booking Info', {'fields': ('user', 'car', 'booking_date', 'booking_time')}),
        ('Status', {'fields': ('status', 'admin_notes')}),
        ('Notes', {'fields': ('notes',)}),
    )
