from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm
from cars.models import Car, Brand
from bookings.models import Booking

def home(request):
    featured_cars = Car.objects.filter(is_available=True).select_related('brand')[:6]
    brands = Brand.objects.all()
    context = {
        'featured_cars': featured_cars,
        'brands': brands,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    bookings = Booking.objects.filter(user=request.user).select_related('car__brand')
    context = {
        'form': form,
        'bookings': bookings,
    }
    return render(request, 'profile.html', context)
