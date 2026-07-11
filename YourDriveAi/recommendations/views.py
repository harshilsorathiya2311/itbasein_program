import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .ml_engine import recommender
from .models import RecommendationLog
from cars.models import Car, Brand

logger = logging.getLogger(__name__)

BODY_CHOICES = ['SUV', 'Sedan', 'Hatchback', 'Coupe', 'Convertible', 'Wagon', 'Crossover', 'Pickup', 'Van']


def _gather_preferences(request):
    prefs = {}

    if request.method == 'POST':
        num_fields = ['min_price', 'max_price', 'min_seating', 'max_mileage', 'safety_priority']
        text_fields = ['brand', 'fuel_type', 'transmission', 'body_type']

        for field in num_fields:
            val = request.POST.get(field)
            if val:
                prefs[field] = val

        for field in text_fields:
            val = request.POST.get(field, '').strip()
            if val:
                prefs[field] = val

    if request.user.is_authenticated and not prefs:
        profile = request.user.profile
        if profile.budget:
            prefs['max_price'] = str(profile.budget)
        if profile.preferred_fuel_type:
            prefs['fuel_type'] = profile.preferred_fuel_type
        if profile.preferred_transmission:
            prefs['transmission'] = profile.preferred_transmission
        if profile.preferred_seating:
            prefs['min_seating'] = str(profile.preferred_seating)
        if profile.preferred_body_type:
            prefs['body_type'] = profile.preferred_body_type
        if profile.safety_priority:
            prefs['safety_priority'] = str(profile.safety_priority)

    return prefs


def recommend_cars(request):
    user_prefs = _gather_preferences(request)
    results = []

    if request.method == 'POST' or (request.method == 'GET' and user_prefs):
        results = recommender.recommend(user_prefs, n=5)

        if request.user.is_authenticated and results:
            try:
                log_entry = RecommendationLog.objects.create(
                    user=request.user,
                    car=results[0]['car'],
                    score=results[0]['score_raw'],
                    method='content_based',
                )
            except Exception as e:
                logger.warning(f'Could not log recommendation: {e}')

    context = {
        'results': results,
        'user_prefs': user_prefs,
        'brands': Brand.objects.all().order_by('name'),
        'body_choices': BODY_CHOICES,
    }
    return render(request, 'recommendations/recommend.html', context)


@login_required
def save_preferences(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.budget = request.POST.get('max_price') or None
        profile.preferred_fuel_type = request.POST.get('fuel_type', '')
        profile.preferred_transmission = request.POST.get('transmission', '')
        profile.preferred_seating = request.POST.get('min_seating') or None
        profile.preferred_body_type = request.POST.get('body_type', '')
        profile.safety_priority = request.POST.get('safety_priority') or None
        profile.save()
        messages.success(request, 'Preferences saved!')
        return redirect('recommend_cars')

    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'recommendations/preferences.html', context)
