import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _send_email(subject, template_name, context, recipient_email):
    if not recipient_email:
        logger.warning('No recipient email provided, skipping notification.')
        return False
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info('Email sent to %s: %s', recipient_email, subject)
        return True
    except Exception as e:
        logger.error('Failed to send email to %s (subject=%s): %s', recipient_email, subject, e)
        return False


def send_booking_confirmation(booking):
    subject = 'YourDriveAi - Test Drive Request Received'
    context = {
        'user': booking.user,
        'car': booking.car,
        'booking': booking,
    }
    return _send_email(subject, 'emails/confirmed.html', context, booking.user.email)


def send_booking_approved(booking):
    subject = 'YourDriveAi - Test Drive Approved'
    context = {
        'user': booking.user,
        'car': booking.car,
        'booking': booking,
        'status': 'Approved',
    }
    return _send_email(subject, 'emails/approved.html', context, booking.user.email)


def send_booking_rejected(booking):
    subject = 'YourDriveAi - Test Drive Request Update'
    context = {
        'user': booking.user,
        'car': booking.car,
        'booking': booking,
        'status': 'Rejected',
    }
    return _send_email(subject, 'emails/rejected.html', context, booking.user.email)


def send_status_update_email(booking, old_status, new_status):
    if new_status == 'Approved':
        return send_booking_approved(booking)
    elif new_status == 'Rejected':
        return send_booking_rejected(booking)
    return False
