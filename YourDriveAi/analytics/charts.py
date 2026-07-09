import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64
from django.conf import settings
from django.db.models import Count, Sum
from cars.models import Car, Brand
from bookings.models import Booking, Review
from analytics.models import UserBehaviorLog
from collections import Counter
from datetime import datetime, timedelta

def generate_chart(fig, filename):
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    path = os.path.join(charts_dir, filename)
    fig.savefig(path, bbox_inches='tight', dpi=100)
    plt.close(fig)
    return os.path.join(settings.MEDIA_URL, 'charts', filename)

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def most_popular_cars_chart():
    car_counts = Booking.objects.values('car__brand__name', 'car__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    if not car_counts:
        return None
    labels = [f"{c['car__brand__name']} {c['car__name']}" for c in car_counts]
    values = [c['count'] for c in car_counts]
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.Greens(np.linspace(0.4, 0.8, len(labels)))
    ax.barh(labels[::-1], values[::-1], color=colors[::-1])
    ax.set_xlabel('Number of Bookings')
    ax.set_title('Most Popular Cars')
    plt.tight_layout()
    return fig_to_base64(fig)

def monthly_bookings_chart():
    three_months_ago = datetime.now() - timedelta(days=90)
    bookings = Booking.objects.filter(created_at__gte=three_months_ago)
    monthly = {}
    for b in bookings:
        key = b.created_at.strftime('%Y-%m')
        monthly[key] = monthly.get(key, 0) + 1
    if not monthly:
        return None
    sorted_months = sorted(monthly.items())
    labels = [m[0] for m in sorted_months]
    values = [m[1] for m in sorted_months]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, values, marker='o', linewidth=2, color='#2563eb')
    ax.fill_between(range(len(labels)), values, alpha=0.3, color='#2563eb')
    ax.set_xlabel('Month')
    ax.set_ylabel('Bookings')
    ax.set_title('Monthly Booking Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig_to_base64(fig)

def brand_performance_chart():
    brand_data = Brand.objects.annotate(car_count=Count('cars')).filter(car_count__gt=0)
    brands = []
    bookings_count = []
    for brand in brand_data:
        count = Booking.objects.filter(car__brand=brand).count()
        if count > 0:
            brands.append(brand.name)
            bookings_count.append(count)
    if not brands:
        return None
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.Blues(np.linspace(0.3, 0.8, len(brands)))
    ax.pie(bookings_count, labels=brands, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Brand Performance (Bookings)')
    plt.tight_layout()
    return fig_to_base64(fig)

def rating_distribution_chart():
    ratings = Review.objects.values('rating').annotate(count=Count('id')).order_by('rating')
    if not ratings:
        return None
    labels = [f"{r['rating']} Star" for r in ratings]
    values = [r['count'] for r in ratings]
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#16a34a']
    ax.bar(labels, values, color=colors[:len(labels)])
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Review Rating Distribution')
    plt.tight_layout()
    return fig_to_base64(fig)

import numpy as np
