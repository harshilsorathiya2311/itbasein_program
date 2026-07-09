from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .ml_engine import recommender
from .models import UserPreference, RecommendationLog
from cars.models import Car

def recommend_cars(request):
    user_prefs = {}

    if request.user.is_authenticated:
        profile = request.user.profile
        user_prefs = {
            'min_price': profile.budget and float(profile.budget) * 0.5,
            'max_price': profile.budget and float(profile.budget),
            'fuel_type': profile.preferred_fuel_type,
            'transmission': profile.preferred_transmission,
            'min_seating': profile.preferred_seating,
        }
        user_prefs = {k: v for k, v in user_prefs.items() if v}

    if request.method == 'POST':
        user_prefs = {
            'min_price': request.POST.get('min_price'),
            'max_price': request.POST.get('max_price'),
            'fuel_type': request.POST.get('fuel_type'),
            'transmission': request.POST.get('transmission'),
            'min_seating': request.POST.get('min_seating'),
            'max_mileage': request.POST.get('max_mileage'),
        }
        user_prefs = {k: v for k, v in user_prefs.items() if v}

    recommended = recommender.content_based_recommend(user_prefs)

    if request.user.is_authenticated:
        for car in recommended:
            RecommendationLog.objects.create(
                user=request.user, car=car,
                score=1.0, method='content_based'
            )

    context = {
        'recommended_cars': recommended,
        'user_prefs': user_prefs,
    }
    return render(request, 'recommendations/recommend.html', context)

@login_required
def save_preferences(request):
    if request.method == 'POST':
        pref, created = UserPreference.objects.get_or_create(user=request.user)
        pref.min_price = request.POST.get('min_price') or None
        pref.max_price = request.POST.get('max_price') or None
        pref.fuel_types = request.POST.get('fuel_types', '')
        pref.transmission = request.POST.get('transmission', '')
        pref.min_seating = request.POST.get('min_seating') or None
        pref.max_mileage = request.POST.get('max_mileage') or None
        pref.save()
    return render(request, 'recommendations/preferences.html', {
        'pref': UserPreference.objects.filter(user=request.user).first()
    })
