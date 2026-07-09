from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fuel_types = models.CharField(max_length=200, blank=True, help_text="Comma-separated")
    transmission = models.CharField(max_length=50, blank=True)
    min_seating = models.IntegerField(null=True, blank=True)
    max_mileage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

class RecommendationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    score = models.FloatField()
    method = models.CharField(max_length=50, default='content_based')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
