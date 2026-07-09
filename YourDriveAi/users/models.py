from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    preferred_fuel_type = models.CharField(max_length=50, blank=True)
    preferred_transmission = models.CharField(max_length=50, blank=True)
    preferred_seating = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
