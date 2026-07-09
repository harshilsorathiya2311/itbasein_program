from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from cars.models import Car


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    dealership = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_notes = models.TextField(blank=True, help_text='Internal notes from admin')
    notes = models.TextField(blank=True, help_text='User notes')
    status_changed_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['booking_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.booking_date})"

    def save(self, *args, **kwargs):
        old_status = None
        if self.pk:
            orig = Booking.objects.filter(pk=self.pk).first()
            if orig and orig.status != self.status:
                old_status = orig.status
                self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)
        if old_status:
            self._send_status_email(old_status, self.status)

    def _send_status_email(self, old_status, new_status):
        if not self.user.email:
            return
        subject = f"YourDriveAi - Booking {new_status.lower()}"
        context = {
            'user': self.user,
            'car': self.car,
            'booking': self,
            'old_status': old_status,
            'new_status': new_status,
        }
        html_message = render_to_string('emails/booking_status.html', context)
        plain_message = f"""
Your test drive booking for {self.car.brand.name} {self.car.name}
on {self.booking_date} at {self.booking_time} has been {new_status.lower()}.

Status: {new_status}
Dealership: {self.dealership or 'TBD'}

Thank you,
YourDriveAi Team
"""
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception:
            pass


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'car']

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.rating}/5)"
