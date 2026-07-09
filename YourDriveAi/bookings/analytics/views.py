from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from cars.models import Car, Brand
from bookings.models import Booking, Review
from analytics.models import UserBehaviorLog
from .charts import (
    most_popular_cars_chart, monthly_bookings_chart,
    brand_performance_chart, rating_distribution_chart,
)

@staff_member_required
def dashboard(request):
    total_cars = Car.objects.count()
    total_bookings = Booking.objects.count()
    total_users = UserBehaviorLog.objects.values('user').distinct().count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    popular_chart = most_popular_cars_chart()
    monthly_chart = monthly_bookings_chart()
    brand_chart = brand_performance_chart()
    rating_chart = rating_distribution_chart()

    recent_bookings = Booking.objects.select_related('user', 'car__brand').order_by('-created_at')[:10]

    context = {
        'total_cars': total_cars,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'avg_rating': round(avg_rating, 1),
        'popular_chart': popular_chart,
        'monthly_chart': monthly_chart,
        'brand_chart': brand_chart,
        'rating_chart': rating_chart,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'analytics/dashboard.html', context)
