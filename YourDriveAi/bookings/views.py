import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.db import IntegrityError
from .models import Booking
from .forms import BookingForm
from cars.models import Car
from recommendations.ml_engine import predictor
from analytics.models import UserBehaviorLog

logger = logging.getLogger(__name__)


@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user_has_pending = Booking.objects.filter(
                user=request.user, car=car, status='Pending'
            ).exists()

            if user_has_pending:
                messages.warning(
                    request,
                    f'You already have a pending request for {car.brand.name} {car.name}. '
                    f'Wait for admin approval or choose another car.'
                )
                return redirect('my_bookings')

            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.car = car
                booking.status = 'Pending'
                booking.save()

                UserBehaviorLog.objects.create(
                    user=request.user, car=car, action='book',
                    session_key=request.session.session_key or ''
                )

                logger.info(
                    f"Booking created: user={request.user.username}, "
                    f"car={car.brand.name} {car.name}, id={booking.id}"
                )

                from .utils import send_booking_confirmation
                send_booking_confirmation(booking)

                messages.success(
                    request,
                    f'Test drive requested for {car.brand.name} {car.name}! '
                    f'Your booking (#{booking.id}) is now pending admin approval. '
                    f'A confirmation email has been sent to {request.user.email}.'
                )
                return redirect('my_bookings')

            except IntegrityError as e:
                logger.error(f"Database error creating booking: {e}")
                messages.error(request, 'A database error occurred. Please try again.')
            except Exception as e:
                logger.error(f"Unexpected error creating booking: {e}")
                messages.error(request, 'Something went wrong. Please try again.')
        else:
            logger.warning(
                f"Invalid booking form from user={request.user.username}: "
                f"{form.errors.as_json()}"
            )
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'car': car,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('car__brand')

    counts = bookings.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='Pending')),
        approved=Count('id', filter=Q(status='Approved')),
        completed=Count('id', filter=Q(status='Completed')),
        rejected=Count('id', filter=Q(status='Rejected')),
    )

    for booking in bookings:
        try:
            pred = predictor.predict_probability({
                'user_bookings': Booking.objects.filter(user=request.user).count(),
                'car_price': float(booking.car.price),
                'car_mileage': float(booking.car.mileage),
                'fuel_type': booking.car.fuel_type,
                'transmission': booking.car.transmission,
                'seating': booking.car.seating_capacity,
                'is_weekend': 1 if booking.booking_date.weekday() >= 5 else 0,
            })
            booking.predicted_probability = pred[0]
            booking.customer_category = pred[1]
        except Exception:
            booking.predicted_probability = None
            booking.customer_category = 'Medium'

    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'counts': counts,
    })


@login_required
def admin_manage_bookings(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')

    status_filter = request.GET.get('status', '')

    bookings = Booking.objects.select_related('user', 'car__brand').all()

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    counts = bookings.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='Pending')),
        approved=Count('id', filter=Q(status='Approved')),
        completed=Count('id', filter=Q(status='Completed')),
        rejected=Count('id', filter=Q(status='Rejected')),
    )

    return render(request, 'admin/manage_bookings.html', {
        'bookings': bookings,
        'counts': counts,
        'current_status': status_filter,
    })


@login_required
def approve_booking(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')

    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status != 'Pending':
        messages.warning(request, f'Booking #{booking.id} is already {booking.status}.')
    else:
        booking.status = 'Approved'
        booking.save()
        messages.success(request, f'Booking #{booking.id} approved successfully.')
    return redirect('admin_manage_bookings')


@login_required
def reject_booking(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')

    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status != 'Pending':
        messages.warning(request, f'Booking #{booking.id} is already {booking.status}.')
    else:
        booking.status = 'Rejected'
        booking.save()
        messages.success(request, f'Booking #{booking.id} rejected.')
    return redirect('admin_manage_bookings')
