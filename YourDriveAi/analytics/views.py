import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from bookings.models import Booking
from .utils import (
    get_dashboard_stats,
    get_brand_car_counts,
    get_booking_status_counts,
    get_monthly_bookings,
    get_popular_cars,
    get_price_analysis,
    get_user_registration_growth,
    get_daily_bookings,
)

logger = logging.getLogger(__name__)


@staff_member_required
def analytics_dashboard(request):
    return render(request, 'analytics/dashboard.html')


@staff_member_required
def api_dashboard_data(request):
    try:
        data = get_dashboard_stats()
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error(f'Dashboard stats API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
def api_brand_analysis(request):
    try:
        data = get_brand_car_counts()
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error(f'Brand analysis API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'data': [], 'error': str(e)})


@staff_member_required
def api_booking_analysis(request):
    try:
        status_data = get_booking_status_counts()
        monthly_data = get_monthly_bookings()
        daily_data = get_daily_bookings(30)
        return JsonResponse({
            'success': True,
            'data': {
                'by_status': status_data,
                'monthly': monthly_data,
                'daily': daily_data,
            }
        })
    except Exception as e:
        logger.error(f'Booking analysis API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'data': {}, 'error': str(e)})


@staff_member_required
def api_popular_cars(request):
    try:
        data = get_popular_cars(10)
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error(f'Popular cars API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'data': [], 'error': str(e)})


@staff_member_required
def api_price_stats(request):
    try:
        data = get_price_analysis()
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error(f'Price stats API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'data': {}, 'error': str(e)})


@staff_member_required
def api_user_growth(request):
    try:
        data = get_user_registration_growth()
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        logger.error(f'User growth API error: {e}', exc_info=True)
        return JsonResponse({'success': False, 'data': [], 'error': str(e)})
