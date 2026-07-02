from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TestDriveBooking
from .forms import BookingForm
from cars.models import Car
from recommendations.models import UserBehavior


@login_required
def book_test_drive(request, car_id=None):
    car = None
    if car_id:
        car = get_object_or_404(Car, pk=car_id)

    initial = {'car': car.pk if car else None}
    form = BookingForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        UserBehavior.objects.create(
            user=request.user, car=booking.car, action='book'
        )
        messages.success(request, f'Test drive booked for {booking.car}! Awaiting approval.')
        return redirect('my_bookings')

    if car:
        form.fields['car'].queryset = Car.objects.filter(pk=car.pk)

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'car': car,
    })


@login_required
def my_bookings(request):
    bookings = TestDriveBooking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(TestDriveBooking, pk=pk, user=request.user)
    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()
        messages.info(request, 'Booking cancelled.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('my_bookings')
