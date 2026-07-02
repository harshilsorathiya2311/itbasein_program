import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YourDrive.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import requests
from cars.models import Car

headers = {'User-Agent': 'YourDrive/1.0 (car-recommendation-app)'}
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'cars')
os.makedirs(media_dir, exist_ok=True)

CAR_WIKI_MAP = {
    'Toyota Camry': 'Toyota Camry',
    'Toyota Fortuner': 'Toyota Fortuner',
    'Toyota Innova Crysta': 'Toyota Innova Crysta',
    'Toyota Corolla': 'Toyota Corolla',
    'Honda City': 'Honda City',
    'Honda CR-V': 'Honda CR-V',
    'Honda Amaze': 'Honda Amaze',
    'Honda Elevate': 'Honda Elevate',
    'Maruti Suzuki Swift': 'Suzuki Swift',
    'Maruti Suzuki Baleno': 'Suzuki Baleno',
    'Maruti Suzuki Grand Vitara': 'Suzuki Grand Vitara',
    'Maruti Suzuki Brezza': 'Suzuki Brezza',
    'Hyundai Creta': 'Hyundai Creta',
    'Hyundai i20': 'Hyundai i20',
    'Hyundai Tucson': 'Hyundai Tucson',
    'Hyundai Venue': 'Hyundai Venue',
    'Tata Motors Nexon': 'Tata Nexon',
    'Tata Motors Harrier': 'Tata Harrier',
    'Tata Motors Punch': 'Tata Punch',
    'Tata Motors Safari': 'Tata Safari',
    'Mahindra Scorpio N': 'Mahindra Scorpio N',
    'Mahindra XUV700': 'Mahindra XUV700',
    'Mahindra Thar': 'Mahindra Thar',
    'BMW 3 Series': 'BMW 3 Series',
    'BMW X1': 'BMW X1',
    'BMW 5 Series': 'BMW 5 Series',
    'Mercedes-Benz C-Class': 'Mercedes-Benz C-Class',
    'Mercedes-Benz GLA': 'Mercedes-Benz GLA',
    'Audi A4': 'Audi A4',
    'Audi Q3': 'Audi Q3',
    'Ford Endeavour': 'Ford Endeavour',
    'Ford Mustang': 'Ford Mustang',
}

def get_wiki_image(search_term):
    params = {
        'action': 'query',
        'format': 'json',
        'titles': search_term,
        'prop': 'pageimages',
        'pithumbsize': 600,
    }
    r = requests.get('https://en.wikipedia.org/w/api.php', params=params, headers=headers, timeout=15)
    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    for pid, page in pages.items():
        if 'thumbnail' in page:
            return page['thumbnail']['source']
    return None

def download_image(url, filepath):
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(r.content)

for car in Car.objects.all():
    search_key = f'{car.brand.name} {car.name}'
    wiki_term = CAR_WIKI_MAP.get(search_key)
    if not wiki_term:
        print(f'SKIP {search_key}: no wiki mapping')
        continue

    image_url = get_wiki_image(wiki_term)
    if not image_url:
        print(f'SKIP {search_key}: no image found on Wikipedia')
        continue

    ext = os.path.splitext(image_url.split('/')[-1].split('?')[0])[1] or '.jpg'
    filename = f'car_{car.id}_{car.brand.name}_{car.name}.{ext}'.replace(' ', '_')
    filepath = os.path.join(media_dir, filename)

    try:
        download_image(image_url, filepath)
        rel_path = f'cars/{filename}'
        car.image = rel_path
        car.save()
        print(f'OK   {search_key} -> {rel_path}')
    except Exception as e:
        print(f'FAIL {search_key}: {e}')
