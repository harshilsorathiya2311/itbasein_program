import logging
from django.db.models import Count, Avg, Min, Max, Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth.models import User
from cars.models import Car, Brand
from bookings.models import Booking

logger = logging.getLogger(__name__)


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return default


def get_dashboard_stats():
    total_cars = Car.objects.count()
    total_brands = Brand.objects.count()
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    approved = Booking.objects.filter(status='Approved').count()
    rejected = Booking.objects.filter(status='Rejected').count()
    pending = Booking.objects.filter(status='Pending').count()

    total = approved + rejected + pending
    approval_rate = round((approved / total * 100) if total > 0 else 0, 1)

    return {
        'total_cars': safe_int(total_cars),
        'total_brands': safe_int(total_brands),
        'total_users': safe_int(total_users),
        'total_bookings': safe_int(total_bookings),
        'approved': safe_int(approved),
        'rejected': safe_int(rejected),
        'pending': safe_int(pending),
        'approval_rate': approval_rate,
    }


def get_brand_car_counts():
    brands = (
        Brand.objects.annotate(
            car_count=Count('cars'),
            booking_count=Count('cars__bookings'),
        )
        .order_by('-car_count')
    )
    max_count = max((b.car_count for b in brands), default=1)
    return [
        {
            'label': b.name,
            'car_count': b.car_count,
            'booking_count': b.booking_count,
            'popularity': round((b.booking_count / max_count) * 100 if max_count > 0 else 0, 1),
        }
        for b in brands
    ]


def get_booking_status_counts():
    total = Booking.objects.count()
    result = []
    for s in ['Approved', 'Rejected', 'Pending', 'Completed']:
        count = Booking.objects.filter(status=s).count()
        if count > 0 or s == 'Pending':
            percentage = round((count / total * 100) if total > 0 else 0, 1) if count > 0 else 0
            result.append({'label': s, 'count': count, 'percentage': percentage})
    return result


def get_monthly_bookings(months=12):
    from django.utils import timezone
    from datetime import timedelta
    cutoff = timezone.now() - timedelta(days=months * 31)
    monthly = (
        Booking.objects
        .filter(created_at__gte=cutoff)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    return [
        {
            'label': m['month'].strftime('%b %Y') if m['month'] else 'Unknown',
            'count': m['count'],
        }
        for m in monthly
    ]


def get_popular_cars(limit=10):
    cars = (
        Car.objects
        .annotate(
            booking_count=Count('bookings'),
        )
        .filter(booking_count__gt=0)
        .order_by('-booking_count')[:limit]
    )
    max_count = max((c.booking_count for c in cars), default=1)
    return [
        {
            'label': f"{c.brand.name} {c.name}",
            'count': c.booking_count,
            'price': safe_float(c.price),
            'popularity': round((c.booking_count / max_count) * 100, 1),
        }
        for c in cars
    ]


def get_price_analysis():
    stats = Car.objects.aggregate(
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price'),
        total_value=Sum('price'),
        car_count=Count('id'),
    )
    avg = safe_float(stats.get('avg_price', 0))
    mn = safe_float(stats.get('min_price', 0))
    mx = safe_float(stats.get('max_price', 0))
    total_val = safe_float(stats.get('total_value', 0))
    count = safe_int(stats.get('car_count', 0))
    return {
        'avg_price': avg,
        'min_price': mn,
        'max_price': mx,
        'total_value': total_val,
        'car_count': count,
    }


def get_user_registration_growth():
    monthly = (
        User.objects
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    running = 0
    result = []
    for m in monthly:
        running += m['count']
        result.append({
            'label': m['month'].strftime('%b %Y') if m['month'] else 'Unknown',
            'count': m['count'],
            'total': running,
        })
    return result


def get_daily_bookings(days=30):
    from django.utils import timezone
    from datetime import timedelta
    cutoff = timezone.now() - timedelta(days=days)
    daily = (
        Booking.objects
        .filter(created_at__gte=cutoff)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    return [
        {
            'label': d['day'].strftime('%d %b') if d['day'] else 'Unknown',
            'count': d['count'],
        }
        for d in daily
    ]
