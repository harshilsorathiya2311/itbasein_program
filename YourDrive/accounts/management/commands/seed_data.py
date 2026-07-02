from django.core.management.base import BaseCommand
from cars.models import Brand, Car
from accounts.models import User
from bookings.models import TestDriveBooking
from datetime import date, time, timedelta
import random


class Command(BaseCommand):
    help = 'Seed database with sample brands, cars, users, and bookings'

    def handle(self, *args, **options):
        brands_data = [
            {'name': 'Toyota', 'country': 'Japan', 'founded_year': 1937},
            {'name': 'Honda', 'country': 'Japan', 'founded_year': 1948},
            {'name': 'Maruti Suzuki', 'country': 'India', 'founded_year': 1981},
            {'name': 'Hyundai', 'country': 'South Korea', 'founded_year': 1967},
            {'name': 'Tata Motors', 'country': 'India', 'founded_year': 1945},
            {'name': 'Mahindra', 'country': 'India', 'founded_year': 1945},
            {'name': 'BMW', 'country': 'Germany', 'founded_year': 1916},
            {'name': 'Mercedes-Benz', 'country': 'Germany', 'founded_year': 1926},
            {'name': 'Audi', 'country': 'Germany', 'founded_year': 1909},
            {'name': 'Ford', 'country': 'USA', 'founded_year': 1903},
        ]

        brands = {}
        for b in brands_data:
            brand, created = Brand.objects.get_or_create(name=b['name'], defaults=b)
            brands[b['name']] = brand
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {brand.name}'))

        cars_data = [
            {'brand': 'Toyota', 'name': 'Camry', 'model_year': 2024, 'price': 4500000, 'fuel_type': 'Petrol', 'transmission': 'Automatic', 'seats': 5, 'mileage': 16.5, 'engine_cc': 2494, 'horsepower': 203},
            {'brand': 'Toyota', 'name': 'Fortuner', 'model_year': 2024, 'price': 3500000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 7, 'mileage': 14.2, 'engine_cc': 2755, 'horsepower': 201},
            {'brand': 'Toyota', 'name': 'Innova Crysta', 'model_year': 2024, 'price': 2800000, 'fuel_type': 'Diesel', 'transmission': 'Manual', 'seats': 7, 'mileage': 15.1, 'engine_cc': 2393, 'horsepower': 148},
            {'brand': 'Toyota', 'name': 'Corolla', 'model_year': 2023, 'price': 2200000, 'fuel_type': 'Petrol', 'transmission': 'CVT', 'seats': 5, 'mileage': 17.8, 'engine_cc': 1798, 'horsepower': 138},
            {'brand': 'Honda', 'name': 'City', 'model_year': 2024, 'price': 1400000, 'fuel_type': 'Petrol', 'transmission': 'CVT', 'seats': 5, 'mileage': 18.4, 'engine_cc': 1498, 'horsepower': 119},
            {'brand': 'Honda', 'name': 'CR-V', 'model_year': 2024, 'price': 3800000, 'fuel_type': 'Petrol', 'transmission': 'CVT', 'seats': 5, 'mileage': 15.4, 'engine_cc': 1996, 'horsepower': 158},
            {'brand': 'Honda', 'name': 'Amaze', 'model_year': 2024, 'price': 850000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 19.5, 'engine_cc': 1199, 'horsepower': 88},
            {'brand': 'Honda', 'name': 'Elevate', 'model_year': 2024, 'price': 1600000, 'fuel_type': 'Petrol', 'transmission': 'CVT', 'seats': 5, 'mileage': 16.5, 'engine_cc': 1498, 'horsepower': 119},
            {'brand': 'Maruti Suzuki', 'name': 'Swift', 'model_year': 2024, 'price': 700000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 22.0, 'engine_cc': 1197, 'horsepower': 88},
            {'brand': 'Maruti Suzuki', 'name': 'Baleno', 'model_year': 2024, 'price': 850000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 21.4, 'engine_cc': 1197, 'horsepower': 88},
            {'brand': 'Maruti Suzuki', 'name': 'Grand Vitara', 'model_year': 2024, 'price': 1500000, 'fuel_type': 'Hybrid', 'transmission': 'Automatic', 'seats': 5, 'mileage': 27.0, 'engine_cc': 1490, 'horsepower': 114},
            {'brand': 'Maruti Suzuki', 'name': 'Brezza', 'model_year': 2024, 'price': 900000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 19.8, 'engine_cc': 1462, 'horsepower': 101},
            {'brand': 'Hyundai', 'name': 'Creta', 'model_year': 2024, 'price': 1600000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 5, 'mileage': 21.0, 'engine_cc': 1493, 'horsepower': 113},
            {'brand': 'Hyundai', 'name': 'i20', 'model_year': 2024, 'price': 850000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 20.0, 'engine_cc': 1197, 'horsepower': 83},
            {'brand': 'Hyundai', 'name': 'Tucson', 'model_year': 2024, 'price': 3500000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 5, 'mileage': 17.0, 'engine_cc': 1995, 'horsepower': 186},
            {'brand': 'Hyundai', 'name': 'Venue', 'model_year': 2024, 'price': 1000000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 19.0, 'engine_cc': 1197, 'horsepower': 83},
            {'brand': 'Tata Motors', 'name': 'Nexon', 'model_year': 2024, 'price': 1000000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 17.5, 'engine_cc': 1497, 'horsepower': 118},
            {'brand': 'Tata Motors', 'name': 'Harrier', 'model_year': 2024, 'price': 2000000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 5, 'mileage': 16.0, 'engine_cc': 1956, 'horsepower': 168},
            {'brand': 'Tata Motors', 'name': 'Punch', 'model_year': 2024, 'price': 700000, 'fuel_type': 'Petrol', 'transmission': 'Manual', 'seats': 5, 'mileage': 18.8, 'engine_cc': 1199, 'horsepower': 86},
            {'brand': 'Tata Motors', 'name': 'Safari', 'model_year': 2024, 'price': 2200000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 7, 'mileage': 15.0, 'engine_cc': 1956, 'horsepower': 168},
            {'brand': 'Mahindra', 'name': 'Scorpio N', 'model_year': 2024, 'price': 1800000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 7, 'mileage': 15.0, 'engine_cc': 2184, 'horsepower': 172},
            {'brand': 'Mahindra', 'name': 'XUV700', 'model_year': 2024, 'price': 2000000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 7, 'mileage': 16.0, 'engine_cc': 2198, 'horsepower': 185},
            {'brand': 'Mahindra', 'name': 'Thar', 'model_year': 2024, 'price': 1500000, 'fuel_type': 'Diesel', 'transmission': 'Manual', 'seats': 4, 'mileage': 14.0, 'engine_cc': 2184, 'horsepower': 130},
            {'brand': 'BMW', 'name': '3 Series', 'model_year': 2024, 'price': 5500000, 'fuel_type': 'Petrol', 'transmission': 'Automatic', 'seats': 5, 'mileage': 15.5, 'engine_cc': 1998, 'horsepower': 255},
            {'brand': 'BMW', 'name': 'X1', 'model_year': 2024, 'price': 5000000, 'fuel_type': 'Petrol', 'transmission': 'DCT', 'seats': 5, 'mileage': 16.0, 'engine_cc': 1998, 'horsepower': 189},
            {'brand': 'BMW', 'name': '5 Series', 'model_year': 2024, 'price': 7500000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 5, 'mileage': 18.0, 'engine_cc': 1995, 'horsepower': 262},
            {'brand': 'Mercedes-Benz', 'name': 'C-Class', 'model_year': 2024, 'price': 6000000, 'fuel_type': 'Petrol', 'transmission': 'Automatic', 'seats': 5, 'mileage': 15.0, 'engine_cc': 1991, 'horsepower': 201},
            {'brand': 'Mercedes-Benz', 'name': 'GLA', 'model_year': 2024, 'price': 5200000, 'fuel_type': 'Petrol', 'transmission': 'DCT', 'seats': 5, 'mileage': 16.0, 'engine_cc': 1991, 'horsepower': 221},
            {'brand': 'Audi', 'name': 'A4', 'model_year': 2024, 'price': 5500000, 'fuel_type': 'Petrol', 'transmission': 'Automatic', 'seats': 5, 'mileage': 16.5, 'engine_cc': 1984, 'horsepower': 201},
            {'brand': 'Audi', 'name': 'Q3', 'model_year': 2024, 'price': 5000000, 'fuel_type': 'Petrol', 'transmission': 'DCT', 'seats': 5, 'mileage': 15.5, 'engine_cc': 1984, 'horsepower': 187},
            {'brand': 'Ford', 'name': 'Endeavour', 'model_year': 2023, 'price': 3500000, 'fuel_type': 'Diesel', 'transmission': 'Automatic', 'seats': 7, 'mileage': 14.5, 'engine_cc': 1996, 'horsepower': 168},
            {'brand': 'Ford', 'name': 'Mustang', 'model_year': 2024, 'price': 7500000, 'fuel_type': 'Petrol', 'transmission': 'Automatic', 'seats': 4, 'mileage': 8.5, 'engine_cc': 4951, 'horsepower': 443},
        ]

        for c in cars_data:
            brand = brands[c['brand']]
            car_defaults = {k: v for k, v in c.items() if k != 'brand'}
            car, created = Car.objects.get_or_create(
                brand=brand, name=c['name'], model_year=c['model_year'],
                defaults=car_defaults
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created car: {car}'))

        users_data = [
            {'username': 'john', 'email': 'john@example.com', 'budget': 1500000},
            {'username': 'jane', 'email': 'jane@example.com', 'budget': 2500000},
            {'username': 'sam', 'email': 'sam@example.com', 'budget': 5000000},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={'email': u['email'], 'budget': u['budget']}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username} / password123'))

        all_cars = list(Car.objects.all())
        users = list(User.objects.filter(is_superuser=False))
        statuses = ['Pending', 'Approved', 'Completed', 'Cancelled']

        for user in users:
            for _ in range(3):
                car = random.choice(all_cars)
                booking, created = TestDriveBooking.objects.get_or_create(
                    user=user,
                    car=car,
                    booking_date=date.today() + timedelta(days=random.randint(1, 30)),
                    booking_time=time(random.randint(9, 17), 0),
                    defaults={'status': random.choice(statuses)}
                )
                if created:
                    self.stdout.write(f'Created booking: {user.username} -> {car}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeded: {Brand.objects.count()} brands, {Car.objects.count()} cars, '
            f'{User.objects.count()} users, {TestDriveBooking.objects.count()} bookings'
        ))
