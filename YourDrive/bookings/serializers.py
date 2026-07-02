from rest_framework import serializers
from .models import TestDriveBooking


class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    car_name = serializers.CharField(source='car.__str__', read_only=True)

    class Meta:
        model = TestDriveBooking
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
