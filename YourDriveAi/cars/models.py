from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True)

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
    ]
    BODY_CHOICES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Wagon', 'Wagon'),
        ('Crossover', 'Crossover'),
        ('Pickup', 'Pickup'),
        ('Van', 'Van'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    mileage = models.DecimalField(max_digits=6, decimal_places=2, help_text="kmpl or km/kWh")
    seating_capacity = models.IntegerField(default=5)
    engine_cc = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    power = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="bhp")
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES, default='Sedan')
    safety_rating = models.IntegerField(default=3, help_text="Safety rating 1-5")
    image = models.ImageField(upload_to='cars/', blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0
