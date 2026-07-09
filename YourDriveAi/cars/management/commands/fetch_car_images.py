import os
import requests
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from cars.models import Car

HEADERS = {"User-Agent": "YourDriveAi/1.0"}
WIKI_API = "https://en.wikipedia.org/w/api.php"

def wiki_request(params):
    for i in range(2):
        try:
            r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(0.5)
    return None

def get_car_image(brand, name):
    data = wiki_request({
        "action": "query", "format": "json", "list": "search",
        "srsearch": f"{brand} {name}", "srlimit": 5
    })
    if not data:
        return None
    for p in data.get("query", {}).get("search", []):
        pi = wiki_request({
            "action": "query", "format": "json", "titles": p["title"],
            "prop": "pageimages", "pithumbsize": 800, "redirects": 1
        })
        if not pi:
            continue
        for pid, pg in pi.get("query", {}).get("pages", {}).items():
            if pid != "-1" and "thumbnail" in pg:
                return pg["thumbnail"]["source"]

    data2 = wiki_request({
        "action": "query", "format": "json", "list": "search",
        "srsearch": f"{name}", "srlimit": 3
    })
    if data2:
        for p in data2.get("query", {}).get("search", []):
            pi = wiki_request({
                "action": "query", "format": "json", "titles": p["title"],
                "prop": "pageimages", "pithumbsize": 800, "redirects": 1
            })
            if not pi:
                continue
            for pid, pg in pi.get("query", {}).get("pages", {}).items():
                if pid != "-1" and "thumbnail" in pg:
                    return pg["thumbnail"]["source"]
    return None

class Command(BaseCommand):
    help = 'Fetch real car images from Wikipedia'

    def handle(self, *args, **options):
        cars = Car.objects.filter(image="").select_related('brand')
        if not cars:
            cars = Car.objects.select_related('brand')

        os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'media', 'cars'), exist_ok=True)

        success = 0
        for i, car in enumerate(cars):
            if car.image and car.image.name:
                continue
            self.stdout.write(f"[{i+1}/{cars.count()}] {car.brand.name} {car.name}...", ending=' ')
            self.stdout.flush()
            img_url = get_car_image(car.brand.name, car.name)
            if img_url:
                try:
                    resp = requests.get(img_url, headers=HEADERS, timeout=20)
                    if resp.status_code == 200 and len(resp.content) > 5000:
                        fn = f"{car.brand.name.lower().replace(' ', '_')}_{car.name.lower().replace(' ', '_').replace(' ', '_')}.jpg"
                        car.image.save(fn, ContentFile(resp.content), save=True)
                        self.stdout.write(self.style.SUCCESS("OK"))
                        success += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"small({len(resp.content)}b)"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"err:{e}"))
            else:
                self.stdout.write(self.style.WARNING("no img"))
            time.sleep(0.3)

        self.stdout.write(self.style.SUCCESS(f"\nDownloaded {success}/{cars.count()} images"))
