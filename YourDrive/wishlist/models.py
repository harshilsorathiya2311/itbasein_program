from django.db import models
from django.conf import settings


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'car']

    def __str__(self):
        return f"{self.user.username} - {self.car}"
