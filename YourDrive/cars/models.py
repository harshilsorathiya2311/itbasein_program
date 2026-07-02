from django.db import models
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('CNG', 'CNG'),
    ]
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
        ('CVT', 'CVT'),
        ('DCT', 'DCT'),
    ]
    SEATS_CHOICES = [(2, '2'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=200)
    model_year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField(choices=SEATS_CHOICES, default=5)
    mileage = models.DecimalField(max_digits=5, decimal_places=2, help_text='kmpl or km/kWh')
    engine_cc = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    horsepower = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, help_text='Comma-separated features')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand', 'name']

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.model_year})"

    def get_absolute_url(self):
        return reverse('car_detail', args=[self.pk])

    def feature_list(self):
        return [f.strip() for f in self.features.split(',')] if self.features else []
