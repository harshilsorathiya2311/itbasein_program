from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .ml_utils import recommend_cars, load_trained_models, train_recommendation_model
from .models import RecommendationLog, UserBehavior
from cars.models import Car
from accounts.models import UserPreference


@login_required
def get_recommendations(request):
    user = request.user
    pref, _ = UserPreference.objects.get_or_create(user=user)

    budget = request.GET.get('budget') or (float(pref.max_budget) if pref.max_budget else None)
    brand = request.GET.get('brand') or pref.preferred_brand or ''
    fuel = request.GET.get('fuel') or pref.preferred_fuel_type or ''
    transmission = request.GET.get('transmission') or pref.preferred_transmission or ''
    algorithm = request.GET.get('algorithm', 'decision_tree')

    recommendations, accuracies = recommend_cars(
        user_budget=budget,
        preferred_brand=brand,
        preferred_fuel=fuel,
        preferred_transmission=transmission,
        algorithm=algorithm,
    )

    car_list = []
    for rec in recommendations:
        try:
            car = Car.objects.get(pk=rec['car_id'])
            car_list.append({
                'car': car,
                'confidence': rec['confidence'],
                'price': rec['price'],
            })
        except Car.DoesNotExist:
            pass

    if car_list:
        RecommendationLog.objects.create(
            user=user,
            recommended_cars=[item['car'].id for item in car_list],
            input_data={'budget': budget, 'brand': brand, 'fuel': fuel, 'transmission': transmission},
            ml_algorithm=algorithm,
            confidence_score=recommendations[0]['confidence'] if recommendations else None,
        )

    return render(request, 'recommendations/recommendations.html', {
        'car_list': car_list,
        'budget': budget,
        'accuracies': accuracies,
        'algorithm': algorithm,
    })


@login_required
def retrain_model(request):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can retrain the model.')
        return redirect('home')

    result = train_recommendation_model()
    if result[0]:
        messages.success(request, 'ML models retrained successfully!')
    else:
        messages.error(request, 'Not enough data to train models.')
    return redirect('dashboard_home')
