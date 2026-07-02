from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Car, Brand
from .forms import CarSearchForm
from recommendations.models import UserBehavior


def car_list(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.filter(is_available=True)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        brand = form.cleaned_data.get('brand')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        fuel_type = form.cleaned_data.get('fuel_type')
        transmission = form.cleaned_data.get('transmission')
        seats = form.cleaned_data.get('seats')

        if query:
            cars = cars.filter(
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(description__icontains=query)
            )
        if brand:
            cars = cars.filter(brand__name=brand)
        if min_price:
            cars = cars.filter(price__gte=min_price)
        if max_price:
            cars = cars.filter(price__lte=max_price)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if transmission:
            cars = cars.filter(transmission=transmission)
        if seats:
            cars = cars.filter(seats=seats)

    # Log user behavior if logged in
    if request.user.is_authenticated and request.GET.get('query'):
        UserBehavior.objects.create(
            user=request.user,
            car=cars.first() if cars.exists() else None,
            action='search'
        )

    brands = Brand.objects.all()
    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'form': form,
        'brands': brands,
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.user.is_authenticated:
        UserBehavior.objects.create(
            user=request.user,
            car=car,
            action='view'
        )

    similar_cars = Car.objects.filter(
        brand=car.brand, is_available=True
    ).exclude(pk=car.pk)[:4]

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'similar_cars': similar_cars,
    })


def compare_cars(request):
    car_ids = request.GET.getlist('ids')
    cars = Car.objects.filter(pk__in=car_ids, is_available=True) if car_ids else []

    if request.user.is_authenticated and cars:
        for car in cars:
            UserBehavior.objects.create(user=request.user, car=car, action='compare')

    return render(request, 'cars/compare.html', {'cars': cars})
