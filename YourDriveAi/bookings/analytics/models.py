from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class UserBehaviorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=[
        ('view', 'View'),
        ('book', 'Book'),
        ('review', 'Review'),
        ('compare', 'Compare'),
    ])
    session_key = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
