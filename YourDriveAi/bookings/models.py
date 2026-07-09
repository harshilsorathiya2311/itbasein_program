import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cars.models import Car

logger = logging.getLogger(__name__)


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
    phone_number = models.CharField(max_length=20, blank=True, help_text='Contact phone number')
    address = models.TextField(blank=True, help_text='Your address')
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
            from .utils import send_status_update_email
            sent = send_status_update_email(self, old_status, self.status)
            if sent:
                logger.info('Status change email sent for booking %s: %s -> %s', self.id, old_status, self.status)
            else:
                logger.warning('Status change email not sent for booking %s', self.id)


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
