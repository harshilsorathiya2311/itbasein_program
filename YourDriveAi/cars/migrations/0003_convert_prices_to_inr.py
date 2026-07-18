from django.db import migrations
from decimal import Decimal


def convert_prices_to_inr(apps, schema_editor):
    Car = apps.get_model('cars', 'Car')
    INR_RATE = Decimal('83.0')
    updated = 0
    for car in Car.objects.all():
        old_price = car.price
        car.price = old_price * INR_RATE
        car.save(update_fields=['price'])
        updated += 1
    if updated:
        print(f'  Converted {updated} car prices from USD to INR (x{INR_RATE})')


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_car_body_type_car_safety_rating'),
    ]

    operations = [
        migrations.RunPython(convert_prices_to_inr, migrations.RunPython.noop),
    ]
