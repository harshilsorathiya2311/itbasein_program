from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def home(request):
    from cars.models import Car, Brand
    from bookings.models import TestDriveBooking
    from reviews.models import Review
    cars = Car.objects.filter(is_available=True).select_related('brand')[:6]
    brands = Brand.objects.all()
    total_cars = Car.objects.count()
    total_users = __import__('django.contrib.auth', fromlist=['get_user_model']).get_user_model().objects.count()
    total_bookings = TestDriveBooking.objects.count()
    total_brands = Brand.objects.count()
    reviews = Review.objects.select_related('user', 'car__brand').all()[:3]
    return render(request, 'home.html', {
        'featured_cars': cars,
        'brands': brands,
        'total_cars': total_cars,
        'total_bookings': total_bookings,
        'total_brands': total_brands,
        'total_users': total_users,
        'reviews': reviews,
    })


def openai_chat(request):
    import json
    from django.http import JsonResponse
    from django.conf import settings
    from openai import OpenAI

    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get('message', '')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return JsonResponse({'reply': 'OpenAI API key not configured. Please set OPENAI_API_KEY in .env'})

    try:
        from cars.models import Car
        cars = Car.objects.filter(is_available=True).select_related('brand')[:20]
        car_list_str = '\n'.join([
            f"- {c.brand.name} {c.name}: ₹{c.price}, {c.fuel_type}, {c.transmission}, {c.mileage} kmpl"
            for c in cars
        ])

        client = OpenAI(api_key=api_key)
        system_prompt = f"""You are a car recommendation assistant for YourDrive. 
Available cars:\n{car_list_str}\n
Help users find their perfect car based on budget, preferences, and needs. Be friendly and concise."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        return JsonResponse({'reply': reply})
    except Exception as e:
        return JsonResponse({'reply': f'Sorry, I encountered an error: {str(e)}'})


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cars/', include('cars.urls')),
    path('bookings/', include('bookings.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reviews/', include('reviews.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/cars/', include('cars.api_urls')),
    path('api/bookings/', include('bookings.api_urls')),
    path('api/recommendations/', include('recommendations.api_urls')),
    path('openai-chat/', openai_chat, name='openai_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
