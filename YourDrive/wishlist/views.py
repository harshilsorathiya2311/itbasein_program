from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Wishlist
from cars.models import Car


@login_required
def toggle_wishlist(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    wish, created = Wishlist.objects.get_or_create(user=request.user, car=car)
    if not created:
        wish.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'removed', 'in_wishlist': False})
        messages.info(request, f'{car} removed from wishlist.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'added', 'in_wishlist': True})
        messages.success(request, f'{car} added to wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'car_list'))


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('car__brand')
    return render(request, 'wishlist/wishlist.html', {'wishlist': items})
