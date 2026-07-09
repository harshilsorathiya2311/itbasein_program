from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review
from cars.models import Car


@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                user=request.user, car=car,
                defaults={'rating': int(rating), 'comment': comment}
            )
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Please provide both rating and comment.')
    return redirect('car_detail', pk=car_id)


@login_required
def delete_review(request, car_id):
    review = get_object_or_404(Review, user=request.user, car_id=car_id)
    review.delete()
    messages.info(request, 'Review deleted.')
    return redirect('car_detail', pk=car_id)
