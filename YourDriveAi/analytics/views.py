from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from bookings.models import Booking
from cars.models import Car, Brand


@staff_member_required
def analytics_dashboard(request):
    total_bookings = Booking.objects.count()
    total_cars = Car.objects.count()
    total_brands = Brand.objects.count()

    bookings_by_status = (
        Booking.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    context = {
        'total_bookings': total_bookings,
        'total_cars': total_cars,
        'total_brands': total_brands,
        'bookings_by_status': bookings_by_status,
    }
    return render(request, 'analytics/dashboard.html', context)
