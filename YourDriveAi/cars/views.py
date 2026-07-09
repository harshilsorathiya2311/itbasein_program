from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Car, Brand
from .forms import CarSearchForm
from bookings.forms import ReviewForm
from bookings.models import Review
from analytics.models import UserBehaviorLog

def car_list(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.filter(is_available=True).select_related('brand')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        fuel_type = form.cleaned_data.get('fuel_type')
        transmission = form.cleaned_data.get('transmission')

        if query:
            cars = cars.filter(
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(description__icontains=query)
            )
        if min_price:
            cars = cars.filter(price__gte=min_price)
        if max_price:
            cars = cars.filter(price__lte=max_price)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if transmission:
            cars = cars.filter(transmission=transmission)

    context = {
        'cars': cars,
        'form': form,
        'brands': Brand.objects.all(),
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car.objects.select_related('brand'), id=car_id)
    reviews = Review.objects.filter(car=car).select_related('user')
    review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('car_detail', car_id=car.id)

    if request.user.is_authenticated:
        UserBehaviorLog.objects.create(
            user=request.user, car=car, action='view',
            session_key=request.session.session_key or ''
        )

    context = {
        'car': car,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'cars/car_detail.html', context)

def car_compare(request):
    car_ids = request.GET.getlist('ids')
    cars = Car.objects.filter(id__in=car_ids).select_related('brand') if car_ids else []
    context = {'cars': cars}
    return render(request, 'cars/car_compare.html', context)

def brand_cars(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    cars = Car.objects.filter(brand=brand, is_available=True).select_related('brand')
    context = {'brand': brand, 'cars': cars}
    return render(request, 'cars/brand_cars.html', context)
