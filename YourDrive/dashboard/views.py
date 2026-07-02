from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from accounts.models import User
from cars.models import Car, Brand
from bookings.models import TestDriveBooking
from recommendations.models import RecommendationLog, UserBehavior
from recommendations.ml_utils import (
    load_trained_models, generate_accuracy_chart,
    generate_booking_trends, train_recommendation_model
)
from datetime import datetime, timedelta
import json


@staff_member_required
def dashboard_home(request):
    total_users = User.objects.count()
    total_cars = Car.objects.count()
    total_brands = Brand.objects.count()
    total_bookings = TestDriveBooking.objects.count()

    pending_bookings = TestDriveBooking.objects.filter(status='Pending').count()
    approved_bookings = TestDriveBooking.objects.filter(status='Approved').count()
    completed_bookings = TestDriveBooking.objects.filter(status='Completed').count()
    cancelled_bookings = TestDriveBooking.objects.filter(status='Cancelled').count()

    # Most booked car
    most_booked = TestDriveBooking.objects.values('car__name', 'car__brand__name').annotate(
        count=Count('id')
    ).order_by('-count').first()

    # Booking trends for last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_bookings = TestDriveBooking.objects.filter(created_at__gte=thirty_days_ago)
    booking_trends_data = []
    for b in recent_bookings:
        booking_trends_data.append({'date': b.created_at.strftime('%Y-%m-%d')})

    booking_chart = generate_booking_trends(booking_trends_data)

    # ML model accuracies
    models_data, _, _, _, accuracies = load_trained_models()
    if models_data is None:
        train_recommendation_model()
        _, _, _, _, accuracies = load_trained_models()

    accuracy_chart = generate_accuracy_chart(accuracies)

    # Recent bookings
    recent_booking_list = TestDriveBooking.objects.select_related('user', 'car__brand').order_by('-created_at')[:10]

    # Popular cars by view behavior
    popular_cars = UserBehavior.objects.filter(action='view').values(
        'car__name', 'car__brand__name'
    ).annotate(count=Count('id')).order_by('-count')[:5]

    # Booking status distribution
    status_data = {
        'Pending': pending_bookings,
        'Approved': approved_bookings,
        'Completed': completed_bookings,
        'Cancelled': cancelled_bookings,
    }

    context = {
        'total_users': total_users,
        'total_cars': total_cars,
        'total_brands': total_brands,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'most_booked_car': most_booked,
        'booking_chart': booking_chart,
        'accuracy_chart': accuracy_chart,
        'accuracies': accuracies,
        'recent_bookings': recent_booking_list,
        'popular_cars': popular_cars,
        'status_data': json.dumps(status_data),
    }
    return render(request, 'dashboard/dashboard_home.html', context)
