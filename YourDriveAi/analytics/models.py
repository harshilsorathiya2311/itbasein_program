from django.db import models
from django.conf import settings
from cars.models import Car


class UserBehaviorLog(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('book', 'Book'),
        ('review', 'Review'),
        ('compare', 'Compare'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    session_key = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user or 'Anonymous'} {self.action}ed {self.car.name}"
