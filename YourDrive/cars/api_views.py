from rest_framework import viewsets, filters
from .models import Car, Brand
from .serializers import CarSerializer, BrandSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.filter(is_available=True).select_related('brand')
    serializer_class = CarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand__name', 'description']
    ordering_fields = ['price', 'mileage', 'model_year', 'name']
    ordering = ['brand__name', 'name']
