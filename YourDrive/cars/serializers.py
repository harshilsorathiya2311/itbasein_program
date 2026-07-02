from rest_framework import serializers
from .models import Car, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_logo = serializers.ImageField(source='brand.logo', read_only=True)

    class Meta:
        model = Car
        fields = '__all__'
