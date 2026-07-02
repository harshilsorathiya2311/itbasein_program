from django.db import models
from django.conf import settings


class RecommendationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations'
    )
    recommended_cars = models.JSONField(help_text='List of recommended car IDs')
    input_data = models.JSONField(help_text='Input features used for recommendation', blank=True, null=True)
    ml_algorithm = models.CharField(max_length=50, help_text='Algorithm used')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.created_at.date()}"


class UserBehavior(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='behaviors'
    )
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='behaviors')
    action = models.CharField(max_length=50, choices=[
        ('view', 'Viewed'),
        ('compare', 'Compared'),
        ('book', 'Booked'),
        ('search', 'Searched'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} {self.action} {self.car}"
