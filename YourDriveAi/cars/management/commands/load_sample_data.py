import csv
import os
from django.core.management.base import BaseCommand
from cars.models import Brand, Car

class Command(BaseCommand):
    help = 'Load sample car data from CSV'

    def handle(self, *args, **options):
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'sample_cars.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"CSV not found at {csv_path}")
            return

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                brand_name = row['brand']
                brand, _ = Brand.objects.get_or_create(name=brand_name)
                Car.objects.get_or_create(
                    brand=brand,
                    name=row['name'],
                    defaults={
                        'price': row['price'],
                        'fuel_type': row['fuel_type'],
                        'transmission': row['transmission'],
                        'mileage': row['mileage'],
                        'seating_capacity': row['seating_capacity'],
                        'engine_cc': row.get('engine_cc') or None,
                        'power': row.get('power') or None,
                        'description': row.get('description', ''),
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Loaded {count} cars from sample data'))
