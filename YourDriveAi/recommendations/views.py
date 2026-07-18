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


def _validate_prefs(prefs):
    """Validate and sanitize user preference values."""
    errors = []

    min_p = prefs.get('min_price')
    max_p = prefs.get('max_price')

    if min_p or max_p:
        try:
            min_val = float(min_p) if min_p else 0
            max_val = float(max_p) if max_p else 0
        except (ValueError, TypeError):
            errors.append('Invalid price values entered.')
            min_val = max_val = 0

        if min_val < 0 or max_val < 0:
            errors.append('Price cannot be negative.')
        if min_val > 0 and max_val > 0 and min_val >= max_val:
            errors.append('Minimum price should be less than maximum price.')
        if min_val > 0 and max_val == 0:
            prefs.pop('min_price', None)

    if prefs.get('min_seating'):
        try:
            s = int(prefs['min_seating'])
            if s < 1 or s > 20:
                errors.append('Seating capacity should be between 1 and 20.')
        except (ValueError, TypeError):
            errors.append('Invalid seating capacity.')

    if prefs.get('safety_priority'):
        try:
            s = int(prefs['safety_priority'])
            if s < 1 or s > 5:
                errors.append('Safety rating should be between 1 and 5.')
        except (ValueError, TypeError):
            errors.append('Invalid safety rating.')

    return errors


def _gather_preferences(request):
    prefs = {}

    if request.method == 'POST':
        num_fields = ['min_price', 'max_price', 'min_seating', 'max_mileage', 'safety_priority']
        text_fields = ['brand', 'fuel_type', 'transmission', 'body_type']

        for field in num_fields:
            val = request.POST.get(field)
            if val or val == '0':
                val = val.strip()
                if val:
                    try:
                        float(val)
                        prefs[field] = val
                    except (ValueError, TypeError):
                        pass

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
    errors = _validate_prefs(user_prefs)
    results = []

    if errors:
        for err in errors:
            messages.warning(request, err)

    if request.method == 'POST' or (request.method == 'GET' and user_prefs):
        if not errors:
            logger.info('=== Price Filter Debug ===')
            logger.info('User prefs: %s', user_prefs)
            logger.info('Total cars in DB: %d', Car.objects.filter(is_available=True).count())

            # Hard ORM-level price filter: convert user INR → DB INR
            min_p = user_prefs.get('min_price')
            max_p = user_prefs.get('max_price')
            if min_p or max_p:
                q = Q(is_available=True)
                if min_p:
                    try:
                        q &= Q(price__gte=float(min_p))
                    except (ValueError, TypeError):
                        pass
                if max_p:
                    try:
                        q &= Q(price__lte=float(max_p))
                    except (ValueError, TypeError):
                        pass
                budget_cars = Car.objects.filter(q).select_related('brand')
                logger.info('ORM price filter: min=%s max=%s → %d cars', min_p, max_p, budget_cars.count())
                if budget_cars.count() == 0:
                    logger.warning('No cars in budget range. Showing empty results.')
                    # Return empty so user sees "no results" message
                    context = {
                        'results': [],
                        'user_prefs': user_prefs,
                        'brands': Brand.objects.all().order_by('name'),
                        'body_choices': BODY_CHOICES,
                    }
                    return render(request, 'recommendations/recommend.html', context)

            results = recommender.recommend(user_prefs, n=5)
            logger.info('Recommend returned %d cars', len(results))
            for r in results:
                logger.info('  Car: %s %s | Price: INR %.0f | Score: %d%%',
                            r['car'].brand.name, r['car'].name,
                            float(r['car'].price), r['score'])

            if request.user.is_authenticated and results:
                try:
                    RecommendationLog.objects.create(
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
